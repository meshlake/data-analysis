import sys
from dataset import set_dataset
from utils.init_logging import init_logging_config
from sql_engine import SqlEngine

if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    # 设置默认数据集
    set_dataset()

    sql_engine = SqlEngine()

    for line in sys.stdin:
        question = line.strip()
        if "q" == question:
            break
        # The LLM takes a prompt as an input and outputs a completion
        answer = sql_engine.invoke(question)

        print(answer)
