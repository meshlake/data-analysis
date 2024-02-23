from llm import llm
import os
import logging

def get_question_query_pair():
    sql_path = os.environ['sql']
    logging.info(f"处理【{sql_path}】的sql数据")

def generate_entity():
    return llm.invoke("你好")