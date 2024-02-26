from generate_entity import generate_entity
from dataset import set_dataset
from utils.init_logging import init_logging_config
from parse_source_table import parse_source_table

if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    # 设置默认数据集
    set_dataset()
    print(parse_source_table())
    # print(generate_entity())