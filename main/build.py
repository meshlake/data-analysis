import logging
from dataset import set_dataset
from utils.init_logging import init_logging_config
import parse_source_table
from entity import Entity
from metrics import Metrics
from dimension import Dimension
from sql_engine import SqlEngine
from utils.util import read_json, write_json_to_file

if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    # 设置默认数据集
    set_dataset()

    logging.info("Start to generate dataset")
    # 生成数据集
    parse_source_table.main(force=True)
    logging.info("Finish to generate dataset")

    logging.info("Start to generate entity")
    # 生成实体
    entity = Entity()
    entity.build_entities(force=True)
    entity.build_vector_store()
    logging.info("Finish to generate entity")

    logging.info("Start to generate metrics")
    # 生成指标
    metrics = Metrics()
    metrics.build_metrics(force=True)
    metrics.build_vector_store()
    logging.info("Finish to generate metrics")
