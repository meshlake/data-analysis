from llm import llm
import os
import logging
from utils.util import read_file
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.output_parsers.json import SimpleJsonOutputParser


def parse_source_table():
    json_parser = SimpleJsonOutputParser()
    chain = llm | json_parser

    messages = [
        SystemMessage(
            content="""
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
                    [
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
                    ]
                    ```
                """
        ),
    ]
    schema = read_file(os.environ["schema"])
    messages.append(HumanMessage(content=f"```{schema}```"))
    # messages.append(
    #     HumanMessage(
    #         content="""
    #         CREATE TABLE `Addresses` (
    #         `address_id` INTEGER PRIMARY KEY,
    #         `line_1` VARCHAR(255),
    #         `line_2` VARCHAR(255),
    #         `line_3` VARCHAR(255),
    #         `city` VARCHAR(255),
    #         `zip_postcode` VARCHAR(20),
    #         `state_province_county` VARCHAR(255),
    #         `country` VARCHAR(255),
    #         `other_address_details` VARCHAR(255)
    #         );
    #         """
    #     )
    # )
    # messages.append(HumanMessage(content=f"你好"))
    # print(messages)
    # source_tables = chain.invoke(messages)
    return chain.invoke(messages)
