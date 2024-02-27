from llm import llm
import os
import logging
from utils.util import read_json, read_file, write_json_to_file, delete_file
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.output_parsers.json import SimpleJsonOutputParser
from output_manage import get_output_path
from tqdm import tqdm
from functools import reduce


def get_question_query_pair():
    """filter sql data

    return:
        list: [{"question": "xxx", "query": "xxx"}]
    """
    sql_path = os.environ["sql"]
    logging.info(f"start parse【{sql_path}】sql data")
    sql_data = read_json(sql_path)
    filter_sql = [
        {"question": item["question"], "query": item["query"]} for item in sql_data
    ]
    logging.info(f"parse【{sql_path}】successful")
    return filter_sql


def generate_entity():
    json_parser = SimpleJsonOutputParser()
    chain = llm | json_parser

    messages = [
        SystemMessage(
            content="""
                    You are an expert in the field of data analysis, proficient in datamesh theory and SQL syntax, 
                    and know that data entities are divided according to business meanings and can be formed by joining one table or multiple tables. 
                    Next, I will give you a table schema of the data field and some sql in this data field. 
                    Please create data entities according to the table given to you, and give the business meaning of these entities, source table and table join sql.
                    Just return the json structure like the example.

                    For example:
                    [
                        {
                            "entityName": "address",
                            "businessSemantics": "Represents the different addresses where students might reside or have lived.",
                            "sourceTable": "["Addresses"]",
                            "joinSql": "SELECT * FROM Addresses",
                        },
                        {
                            "entityName": "Student Enrolment Courses",
                            "businessSemantics": "Links student enrollments to specific courses.",
                            "sourceTable": "["Student_Enrolment_Courses","Courses"]",
                            "joinSql": "SELECT * FROM Student_Enrolment_Courses JOIN Courses ON Student_Enrolment_Courses.course_id = Courses.course_id",
                        }
                    ]
                """
        ),
    ]
    schema = read_file(os.environ["schema"])
    sql = get_question_query_pair().__str__()
    messages.append(HumanMessage(content=f"```{schema}```\n```{sql}```"))
    return chain.invoke(messages)


def find_source_table(table_names: list[str], source_tables: list):
    return [
        source_table
        for source_table in source_tables
        if source_table["name"] in table_names
    ]


def parse_entity(original_entities: list):
    source_tables = read_json(get_output_path("source_table.json"))
    entity_file = get_output_path("entities.json")
    delete_file(entity_file)
    entities = []
    try:
        for entity in tqdm(original_entities):
            entity_source_table_names = entity["sourceTable"]
            entity_source_tables = find_source_table(
                entity_source_table_names, source_tables
            )
            entity["fields"] = reduce(
                lambda x, y: x + y,
                [source_table["fields"] for source_table in entity_source_tables],
            )
            entities.append(entity)
        write_json_to_file(entities, entity_file)
    except Exception as e:
        logging.error(f"parse entity error: {e}")
        write_json_to_file(entities, entity_file)


def main():
    orginal_file = get_output_path("orginal_entities.json")
    delete_file(orginal_file)
    entities = generate_entity()
    write_json_to_file(entities, orginal_file)
    parse_entity(entities)