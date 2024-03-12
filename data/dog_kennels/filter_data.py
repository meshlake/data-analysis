import json
import os

# 过滤dev.json中的数据，只保留db_id为student_transcripts_tracking的数据，并将过滤后的数据写入sql.json文件
def filter():

    # 获取当前文件的目录
    current_dir = os.path.dirname(__file__)

    # 根据相对路径生成绝对路径
    dev_json_path = os.path.abspath(os.path.join(current_dir, '../dev.json'))

    # 读取dev.json文件中的数据
    with open(dev_json_path, 'r') as file:
        data = json.load(file)

    # 过滤出db_id为student_transcripts_tracking的数据
    filtered_data = [item for item in data if item['db_id'] == 'dog_kennels']

    sql_json_path = os.path.abspath(os.path.join(current_dir, './sql.json'))
    # 将过滤后的数据写入新的sql.json文件
    with open(sql_json_path, 'w') as file:
        json.dump(filtered_data, file, indent=4)

if __name__ == '__main__':
    filter()