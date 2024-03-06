from dataset import set_dataset
from utils.init_logging import init_logging_config
import parse_source_table
from entity import Entity
from metrics import Metrics
from dimension import Dimension
from sql_engine import SqlEngine

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
    # entity.build_vector_store()
    # search_entity = entity.search_by_natural_language(
    #     "show me the addresses of the customers"
    # )
    # print(search_entity)

    # 查找实体
    # searched_entities = Entity.search(["Addresses"])
    # print(searched_entities)

    # 生成指标
    # metrics = Metrics()
    # metrics.build_metrics()
    # metrics.build_vector_store()
    # search_metric = metrics.search_by_natural_language(
    #     "show me the addresses of the customers"
    # )
    # print(search_metric)

    # 生成维度
    # dimension = Dimension()
    # dimension.build_dimensions()

    sql_engine = SqlEngine()
    sql = sql_engine.invoke(
        "Find the kind of program which most number of students are enrolled in?"
    )
    print(sql)
