from dataset import set_dataset
from utils.init_logging import init_logging_config
import parse_source_table
import generate_entity
from metrics import Metrics

if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    # 设置默认数据集
    set_dataset()

    # 生成数据集
    # parse_source_table.main()

    # 生成实体
    # generate_entity.main()

    # 生成指标
    metrics = Metrics()
    metrics.build_orginal_metrics()
