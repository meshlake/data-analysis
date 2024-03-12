from dataset import set_dataset
from utils.init_logging import init_logging_config
from sql_engine import SqlEngine
from utils.util import read_json, write_json_to_file

if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    # 设置默认数据集
    set_dataset()

    sql_engine = SqlEngine()

    questions = read_json("question/student.json")
    res = []
    for question in questions:
        sql = sql_engine.invoke(question)
        res.append(sql)

    write_json_to_file(res, "question/student_res.json")
