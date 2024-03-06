import logging
import os
from llm import ChatModel
from output_manage import get_output_path, get_vector_store_path
from utils.util import read_json, write_json_to_file, delete_file
from tqdm import tqdm
from langchain_core.exceptions import OutputParserException
from entity import Entity
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


class Metrics:

    orginal_storage = "orginal_metrics.json"
    storage = "metrics.json"
    vector_store_path = get_vector_store_path()
    
    def __init__(self):
        prompt = """
                You are a data analysis expert who is proficient in SQL. 
                
                An "metric" (also called a indicator or KPI) is a numerical value used to measure business performance, progress, or other key data points. 
                
                Metrics are typically quantifiable and can be used to track and evaluate performance along specific dimensions. 
                
                For example, sales, profit margins, customer satisfaction, etc. are all common business indicators.

                Please find the metrics definition from the sql given to you and return the json structure in the sample.
                If the query does not contain a valid metric, return {"isValid": "False"}.

                For example:
                input: 
                ```
                question: "What is the average score of all students?"
                query: "SELECT AVG(score) FROM student_scores"
                ```

                output:
                ```
                {
                    "name": "student_average_score",
                    "businessSemantics": "average score of all students",
                    "sourceTable": ["student_scores"],
                    "aggregation": "AVG",
                    "field": "score",
                    "dataType": "FLOAT",
                    "isValid": "True",
                    "original": {
                        "question": "What is the average score of all students?",
                        "query": "SELECT AVG(score) FROM student_scores"
                    }
                }
                ```


                input: 
                ```
                question: "what are all the addresses including line 1 and line 2?"
                query: "SELECT line_1 ,  line_2 FROM addresses"
                ```

                output:
                ```
                {
                    "isValid": "False",
                }
                ```
            """

        self.builder = ChatModel(prompt=prompt, is_json_output=True)

        find_entity_prompt = """
            You are an expert in the field of data analysis, proficient in datamesh theory and SQL syntax.

            Please select the best business entity that can calculate the metric from the following business entity definitions based on the indicator definition. 
            
            The metric may be calculated by a single entity or by joining multiple entities.

            Please follow the steps below to process the input data and give the output
            Step 1: Filter out duplicate business entities
            Step 2: Find business entities that meet the definition
            Step 3: Build the business entity json structure to be returned
            Step 4: Check whether the structure to be returned meets the json requirements. If not, go back to step 3.
            Step 5: Return the structure

            For example:

            input:
            ```
                metric:
                ```
                {
                    "name": "total_courses_count",
                    "businessSemantics": "total number of courses listed",
                    "sourceTable": [
                        "Courses"
                    ],
                    "aggregation": "COUNT",
                    "field": "*",
                    "dataType": "INTEGER",
                    "isValid": "True",
                    "original": {
                        "question": "How many courses in total are listed?",
                        "query": "SELECT count(*) FROM Courses"
                    }
                }
                ```

                entities:
                ```
                [
                    {
                        "name": "Courses",
                        "businessSemantics": "Represents the academic courses offered by an educational institution.",
                        "sourceTable": [
                            "Courses"
                        ],
                        "joinSql": "SELECT * FROM Courses",
                        "fields": ["course_id","course_name","course_description","other_details"]
                    },
                    {
                        "name": "Sections",
                        "businessSemantics": "Represents the different sections or groups within a course, potentially offered at different times or by different instructors.",
                        "sourceTable": [
                            "Sections",
                            "Courses"
                        ],
                        "joinSql": "SELECT * FROM Sections JOIN Courses ON Sections.course_id = Courses.course_id",
                        "fields": ["course_id","course_name","course_description","other_details","section_id","section_name","section_description"]
                    },
                ]
                ```
            ```

            output json structure:
            [
                {
                    "name": "Courses",
                }
            ]
        """

        self.entity_searcher = ChatModel(prompt=find_entity_prompt, is_json_output=True)

    def __load_requirements(self):
        """filter sql data

        return:
            list: [{"question": "xxx", "query": "xxx"}]
        """
        sql_path = os.environ["sql"]
        sql_data = read_json(sql_path)
        filter_sql = [
            {"question": item["question"], "query": item["query"]} for item in sql_data
        ]
        return filter_sql

    def __build_orginal_metrics(self):
        sql = self.__load_requirements()
        orginal_metrics = []
        file = get_output_path(self.orginal_storage)
        delete_file(file)

        try:
            for item in tqdm(sql):
                try:
                    metrics = self.builder.invoke(f"```{item}```")
                except OutputParserException:
                    pass
                if metrics["isValid"] == "True":
                    orginal_metrics.append(metrics)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            write_json_to_file(orginal_metrics, file)

        return orginal_metrics

    def build_metrics(self, force=False):
        if not force and os.path.exists(get_output_path(self.orginal_storage)):
            logging.info("Orginal metrics already exists, skip building")
            orginal_metrics = read_json(get_output_path(self.orginal_storage))
        else:
            orginal_metrics = self.__build_orginal_metrics()

        def associate_entities(metric):

            # 找到和指标任意一个sourceTable相关的实体
            associated_entities = [
                entity
                for source_table in metric["sourceTable"]
                for entity in Entity.search_by_source_tables([source_table])
            ]

            # 提取实体的字段名称，过滤无用数据
            def extract_fields(entity):
                entity["fields"] = [field["name"] for field in entity["fields"]]
                return entity

            # 去重并简化实体结构
            associated_entities = [
                extract_fields(entity) for entity in associated_entities
            ]

            # 删除开发字段
            del metric["isValid"]

            llm_selected_entity = self.entity_searcher.invoke(
                f"```{metric}```\n```{associated_entities}```"
            )

            metric["entities"] = [entity["name"] for entity in llm_selected_entity]
            metric["category"] = "METRIC"

            return metric

        metrics = [associate_entities(metric) for metric in tqdm(orginal_metrics)]

        delete_file(get_output_path(self.storage))
        write_json_to_file(metrics, get_output_path(self.storage))

        return metrics

    def build_vector_store(self, force=False):

        if not force and os.path.exists(get_output_path(self.storage)):
            loader = JSONLoader(
                file_path=get_output_path(self.storage),
                jq_schema=".[]",
                text_content=False,
            )
            metrics = loader.load()

            def add_metadata(metric):
                metric.metadata["category"] = "METRIC"
                return metric

            metrics = [add_metadata(metric) for metric in metrics]
        else:
            logging.warning("metrics not found, skip building vector store")

        Chroma.from_documents(
            metrics,
            OpenAIEmbeddings(),
            persist_directory=self.vector_store_path,
            collection_name="metrics",
        )

    @classmethod
    def search_by_natural_language(cls, query: str = ""):
        vector_store = Chroma(
            persist_directory=cls.vector_store_path,
            embedding_function=OpenAIEmbeddings(),
            collection_name="metrics",
        )
        docs = vector_store.similarity_search(query)
        return docs
