import os
import logging

DEFAULT_DATASET = "default"
# 获取当前文件的目录
current_dir = os.path.dirname(__file__)


def set_dataset(dataset: str = None):
    dataset_path = dataset if dataset else DEFAULT_DATASET
    logging.info(f"set dataset【{dataset_path}】")
    # 设置环境变量
    os.environ["schema"] = os.path.abspath(
        os.path.join(current_dir, f"../data/{dataset_path}/schema.sql")
    )
    os.environ["sql"] = os.path.abspath(
        os.path.join(current_dir, f"../data/{dataset_path}/sql.json")
    )
