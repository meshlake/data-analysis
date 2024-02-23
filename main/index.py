from generate_entity import generate_entity, get_question_query_pair
from dataset import set_dataset
from utils.init_logging import init_logging_config


if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()
    
    # 设置默认数据集
    set_dataset()
    get_question_query_pair()
    # print(generate_entity())