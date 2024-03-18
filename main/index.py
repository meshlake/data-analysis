from dataset import set_dataset
from utils.init_logging import init_logging_config
from sql_engine import SqlEngine
from utils.util import read_json, write_json_to_file
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    # 设置默认数据集
    set_dataset()

    sql_engine = SqlEngine()

    question_pairs = read_json("question/gemini_question.json")
    res = []
    for question_pair in question_pairs:
        question = question_pair["question"]
        sql = sql_engine.invoke(question)
        sql["original_query"] = question_pair["query"]
        res.append(sql)

    write_json_to_file(res, "question/student_res.json")
