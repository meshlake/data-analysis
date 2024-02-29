from dataset import set_dataset
from utils.init_logging import init_logging_config
import parse_source_table
from entity import Entity
from metrics import Metrics
from dimension import Dimension

if __name__ == "__main__":
    # 初始化日志配置
    init_logging_config()

    # 设置默认数据集
    set_dataset()

    # 生成数据集
    # parse_source_table.main()

    # 生成实体
    # entity = Entity()
    # entity.build_entities()

    # 查找实体
    # searched_entities = Entity.search(["Addresses"])
    # print(searched_entities)

    # 生成指标
    metrics = Metrics()
    metrics.build_metrics()

    # 生成维度
    # dimension = Dimension()
    # dimension.build_dimensions()
