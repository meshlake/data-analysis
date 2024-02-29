import logging
import os
from llm import ChatModel
from output_manage import get_output_path
from utils.util import read_json, write_json_to_file, delete_file
from tqdm import tqdm
from langchain_core.exceptions import OutputParserException
from entity import Entity


class Metrics:

    orginal_storage = "orginal_metrics.json"
    storage = "metrics.json"

    def __init__(self):
        prompt = """
                You are a data analysis expert who is proficient in SQL. 
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
                    "sourceTable": "student_scores",
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

    def build_metrics(self):
        orginal_metrics = self.__build_orginal_metrics()

        def associate_entities(metric):
            associated_entities = Entity.search(metric["sourceTable"])
            del metric["isValid"]
            metric["entities"] = [entity["name"] for entity in associated_entities]
            return metric

        metrics = [associate_entities(metric) for metric in orginal_metrics]

        delete_file(get_output_path(self.storage))
        write_json_to_file(metrics, get_output_path(self.storage))

        return metrics
