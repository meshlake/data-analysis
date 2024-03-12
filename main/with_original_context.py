import time
import pandas as pd
from llm import ChatModel
from utils.init_logging import init_logging_config
from sql_engine import SqlEngine
from output_manage import get_output_path
from tqdm import tqdm
from utils.util import read_json, write_json_to_file, delete_file


def generate_res(input: str, output: str):

    # 读取Excel文件
    df = pd.read_excel(input)

    data_list = df.values.tolist()

    res = []

    sql_engine = SqlEngine()

    for data in tqdm(data_list):
        question = data[0]
        query = data[1]
        llm_query = data[2]
        is_same = data[3]

        context = sql_engine.get_context(question)

        llm = ChatModel(
            prompt="""
            你是一位DBA高手，我每次会给你两条sql语句，请按照以下步骤判断两条sql是否一致。

            第一步：理解两条sql语句的含义，并构建测试数据。
            第二步：模拟执行两条sql语句，并对比执行结果。
            第三步：根据执行结果返回判断并给出理由。

            """,
            is_json_output=False,
        )
        try:
            reason = llm.invoke(f"1. {query}\n2. {llm_query}").content
        except Exception as e:
            print(e)
            reason = "Error"

        res.append(
            {
                "question": question,
                "query": query,
                "llm_query": llm_query,
                "is_same": is_same,
                "entities": context["entities"],
                "metrics": context["metrics"],
                "reason": reason,
            }
        )

    # 将列表转换为DataFrame
    df = pd.DataFrame(res)

    # 将DataFrame写入Excel文件
    df.to_excel(output, index=False)


def test(file_path: str, type: int = 0):
    metrics = read_json(get_output_path("metrics.json"))

    metrics_original = [metric["original"] for metric in metrics]
    
    sql_engine = SqlEngine()

    test_res = []

    llm = ChatModel(
        prompt="""
        你是一位DBA高手，我每次会给你两条sql语句，请按照以下步骤判断两条sql是否一致。

        第一步：理解两条sql语句的含义，并构建测试数据。
        第二步：模拟执行两条sql语句，并对比执行结果。
        第三步：如果执行结果一致，请返回True，否则返回False。

        结果只返回True或False，不要返回其他信息。
        """,
        is_json_output=False,
    )

    for original in tqdm(metrics_original):
        time.sleep(0.5)
        question = original["question"]

        try:
            if type == 0:
                res = sql_engine.invoke_without_original(question)
            else:
                res = sql_engine.invoke(question)
        except Exception as e:
            print(e)
            test_res.append(
                {
                    "question": question,
                    "query": "Error",
                    "llm_query": "Error",
                    "is_same": "Error",
                }
            )
            continue

        query = original["query"]

        llm_query = res["query"]

        is_same = llm.invoke(f"1. {query}\n2. {llm_query}").content

        test_res.append(
            {
                "question": question,
                "query": query,
                "llm_query": llm_query,
                "is_same": is_same,
            }
        )

    # 将列表转换为DataFrame
    df = pd.DataFrame(test_res)

    # 将DataFrame写入Excel文件
    df.to_excel(file_path, index=False)


if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    for i in range(10):
        no_original_output = f"res1/no_original_{i}.xlsx"
        test(no_original_output, 0)
        with_original_output = f"res1/with_original_{i}.xlsx"
        test(with_original_output, 1)

    # with_original_input = "with_original_context.xlsx"
    # with_original_output = "with_original_context_res.xlsx"
    # generate_res(with_original_input, with_original_output)

    # no_original_input = "no_original_context.xlsx"
    # no_original_output = "no_original_context_res.xlsx"
    # generate_res(no_original_input, no_original_output)
