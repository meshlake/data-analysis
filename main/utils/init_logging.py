import logging

def init_logging_config():
    # 设置日志格式，包括时间、执行文件名和日志级别
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )