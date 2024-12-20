from langchain_community.vectorstores import Chroma
from llm import ChatModel
from output_manage import get_vector_store_path
from langchain_openai import OpenAIEmbeddings
import json


class SqlEngine:
    vector_store_path = get_vector_store_path()

    def __init__(self):

        prompt = """
            You are an expert in data analysis and SQL syntax, and are good at datamesh theory.
            I'll give you some structure for business entities, metrics, and dimensions.
            
            Rule: 
            1.The field of groupby should be appropriately selected according to the problem, usually an identifier or a unique column
            2.Entity does not exist in the actual database. Please use Entity's SourceTables to generate sql statements based on the business meaning of Entity.

            Please follow the steps below to generate sql statements based on the user's questions and these structural information.
            Step 1: Understand the user’s problem
            Step 2: Understand the structural information given to you
            Step 3: Generate sql that conforms to the rules
            Step 4: Check the SQL syntax and whether it violates the rules. 
                    If the syntax is incorrect or the rules are violated, go back to step 3.
            Step 5: Return the question and sql in the sample json format

            
            
            For example:
            input:
            ```
            question: "How many courses in total are listed?"

            entities: {
                "name": "Courses",
                "businessSemantics": "Represents the academic courses offered by an educational institution.",
                "sourceTable": [
                    "Courses"
                ],
                "joinSql": "SELECT * FROM Courses",
                "fields": [
                    {
                        "name": "course_id",
                        "description": "course id",
                        "dataType": "INTEGER",
                        "nullable": "False",
                        "primaryKey": "True",
                        "foreignKey": "False"
                    },
                    {
                        "name": "course_name",
                        "description": "course name",
                        "type": "VARCHAR(255)",
                        "nullable": "False",
                        "primaryKey": "False",
                        "foreignKey": "False"
                    },
                    {
                        "name": "course_description",
                        "description": "course description",
                        "type": "VARCHAR(255)",
                        "nullable": "False",
                        "primaryKey": "False",
                        "foreignKey": "False"
                    },
                    {
                        "name": "other_details",
                        "description": "other details",
                        "type": "VARCHAR(255)",
                        "nullable": "True",
                        "primaryKey": "False",
                        "foreignKey": "False"
                    }
                ]
            }

            metrics: {
                "name": "total_courses_count",
                "businessSemantics": "total number of courses listed",
                "sourceTable": [
                    "Courses"
                ],
                "aggregation": "COUNT",
                "field": "*",
                "dataType": "INTEGER",
                "original": {
                    "question": "How many courses in total are listed?",
                    "query": "SELECT count(*) FROM Courses"
                },
                "entities": [
                    "Courses"
                ]
            }
            ```

            output:
            ```
            {
                "question": "How many courses in total are listed?",
                "query": "SELECT count(*) FROM Courses"
            }
            ```
        """

        self.llm = ChatModel(prompt=prompt, is_json_output=True)

        self.entity_searcher = Chroma(
            persist_directory=self.vector_store_path,
            embedding_function=OpenAIEmbeddings(),
            collection_name="entities",
        )

        self.metric_searcher = Chroma(
            persist_directory=self.vector_store_path,
            embedding_function=OpenAIEmbeddings(),
            collection_name="metrics",
        )

    def invoke(self, question: str):
        # TODO: parse question and extract entities and metrics

        entities = self.entity_searcher.similarity_search(query=question)
        metrics = self.metric_searcher.similarity_search(query=question)

        return self.llm.invoke(
            f"```question:{question}\nentity:{entities}\nmetric:{metrics}```"
        )

    def invoke_without_original(self, question: str):
        # TODO: parse question and extract entities and metrics

        entities = self.entity_searcher.similarity_search(query=question)
        metrics = self.metric_searcher.similarity_search(query=question)

        def delete_original(metric):
            new_metric = json.loads(metric.page_content)
            del new_metric["original"]
            return new_metric

        metrics = [delete_original(metric) for metric in metrics]

        return self.llm.invoke(
            f"```question:{question}\nentity:{entities}\nmetric:{metrics}```"
        )

    def get_context(self, question: str):
        entities = self.entity_searcher.similarity_search(query=question)
        metrics = self.metric_searcher.similarity_search(query=question)

        return {
            "entities": entities,
            "metrics": metrics,
        }
