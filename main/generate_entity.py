from llm import llm
import os
import logging
from utils.util import read_json, read_file
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.output_parsers.json import SimpleJsonOutputParser

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

                    For example:
                    [
                        {
                            "entityName": "address",
                            "businessSemantics": "Represents the different addresses where students might reside or have lived.",
                            "sourceTable": "["Addresses"]",
                            "joinSql": "SELECT * FROM Addresses"
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
    # output1 = chain.invoke(messages)
    # print(output1)
    # messages.append(AIMessage(content=f"```{output1}```"))
    # messages.append(HumanMessage(content="请标明这些实体之间的关联字段和关联关系。"))
    # entities = chain.invoke(messages)
    return chain.invoke(messages)
