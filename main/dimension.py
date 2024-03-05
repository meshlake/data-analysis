import os

from tqdm import tqdm
from llm import ChatModel
from entity import Entity
from output_manage import get_output_path
from utils.util import delete_file, read_json, write_json_to_file
from langchain_core.exceptions import OutputParserException


class Dimension:

    orginal_storage = "orginal_dimensions.json"
    storage = "dimensions.json"

    def __init__(self):
        prompt = """
                You are a data analysis expert who is proficient in SQL. 

                A "dimension" usually refers to a specific aspect of data that is used to classify, group, or describe the data. 
                It can be viewed as an attribute of the data, such as time, location, product type, etc. 
                Dimensions are often used in data warehouses and data cubes to help analysts perform multi-dimensional analysis of data to better understand the characteristics and trends of the data.

                Please find the dimension definition from the sql given to you and return the json structure in the sample.
                If the query does not contain a valid dimension, return {"isValid": "False"}.

                For example:
                input: 
                ```
                query: "SELECT order_date, COUNT(*) AS order_count FROM orders GROUP BY order_date"
                ```

                output:
                ```
                {
                    "name": "date",
                    "businessSemantics": "date",
                    "sourceTable": ["orders"],
                    "field": "order_date",
                    "dataType": "DATE",
                    "isValid": "True",
                    "original": {
                        "question": ""
                        "query": "SELECT order_date, COUNT(*) AS order_count FROM orders GROUP BY order_date"
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

    def __build_orginal_dimensions(self):
        sql = self.__load_requirements()
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
        orginal_dimensions = self.__build_orginal_dimensions()

        def associate_entities(dimension):
            associated_entities = Entity.search(dimension["sourceTable"])
            del dimension["isValid"]
            dimension["entities"] = [entity["name"] for entity in associated_entities]
            return dimension

        dimensions = [associate_entities(dimension) for dimension in orginal_dimensions]

        delete_file(get_output_path(self.storage))
        write_json_to_file(dimensions, get_output_path(self.storage))
        
        return dimensions
