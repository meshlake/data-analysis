import os

from tqdm import tqdm
from llm import ChatModel
from output_manage import get_output_path
from utils.util import delete_file, read_json, write_json_to_file
from langchain_core.exceptions import OutputParserException


class Dimension:
    def __init__(self):
        prompt = """
                You are a data analysis expert who is proficient in SQL. 
                Please find the dimension definition from the sql given to you and return the json structure in the sample.
                If the query does not contain a valid dimension, return {"isValid": "False"}.

                For example:
                input: 
                ```
                question: "What is the average score of every course?"
                query: "SELECT AVG(score) FROM student_scores GROUP BY course_id"
                ```

                output:
                ```
                {
                    "name": "student_course",
                    "businessSemantics": "average score of the course",
                    "sourceTable": "student_scores",
                    "field": "course_id",
                    "dataType": "String",
                    "isValid": "True",
                    "original": {
                        "question": "What is the average score of every course?"
                        "query": "SELECT AVG(score) FROM student_scores GROUP BY course_id"
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

        self.storage = "orginal_dimensions.json"

    def load_requirements(self):
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

    def __build_orginal_dimensions(self):
        sql = self.load_requirements()
        orginal_dimensions = []
        file = get_output_path(self.storage)
        delete_file(file)
        try:
            for item in tqdm(sql):
                try:
                    dimension = self.builder.invoke(f"```{item}```")
                    if dimension["isValid"] == "True":
                        orginal_dimensions.append(dimension)
                except OutputParserException:
                    pass
        except Exception as e:
            print(f"Error: {e}")
        finally:
            write_json_to_file(orginal_dimensions, file)

        return orginal_dimensions

    def build_dimensions(self):
        return self.__build_orginal_dimensions()
