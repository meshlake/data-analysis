import json
import re
from llm import ChatModel
import os
import logging
from utils.util import read_file, write_json_to_file, delete_file
from tqdm import tqdm
from output_manage import get_output_path


def get_table_schema_list():
    schema = read_file(os.environ["schema"])
    # 正则表达式匹配CREATE TABLE语句
    pattern = re.compile(r"CREATE TABLE.*?;", re.DOTALL)

    table_statements = pattern.findall(schema)
    return table_statements


def parse_source_table_schema(table_schema: str):
    prompt = """
        You are a senior SQL engineer. 
        Please change the table schema given to you into the json structure in the example.

        For example:
        input: ```CREATE TABLE `Courses` (
            `course_id` INTEGER PRIMARY KEY,
            `course_name` VARCHAR(255),
            `course_description` VARCHAR(255),
            `other_details` VARCHAR(255)
        );```
        output:
        ```
            {
                "name": "Courses",
                "businessSemantics": "course information",
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
        ```
    """

    llm = ChatModel(prompt=prompt, is_json_output=True)

    return llm.invoke(f"```{table_schema}```")


def generate_source_table_structure():
    table_schema_list = get_table_schema_list()
    file = get_output_path("source_table.json")
    delete_file(file)
    soure_table_structures = []
    try:
        for table_schema in tqdm(table_schema_list):
            soure_table_structure = parse_source_table_schema(table_schema)
            soure_table_structures.append(soure_table_structure)
        write_json_to_file(soure_table_structures, file)
    except Exception as e:
        write_json_to_file(soure_table_structures, file)
        print(f"Error: {e}")


def main(force=False):
    if not force and os.path.exists(get_output_path("source_table.json")):
        logging.info("Source table already exists, skip building")
    else:
        generate_source_table_structure()
