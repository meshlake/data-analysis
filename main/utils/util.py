import json
import os


def read_json(filename):
    """读取JSON文件中的数据。

    参数:
        filename (str): JSON文件的路径。

    返回:
        dict: JSON文件中的数据。
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"文件 {filename} 不存在。")
    except json.JSONDecodeError:
        print(f"文件 {filename} 不是有效的JSON格式。")


def read_file(filename):
    """读取文件中的数据。

    参数:
        filename (str): JSON文件的路径。

    返回:
        str
    """
    try:
        with open(filename, "r") as file:
            file_data = file.read()
        return file_data
    except FileNotFoundError:
        print(f"文件 {filename} 不存在。")

def write_json_to_file(json_data, file_path):
    with open(file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

def append_json_to_file(json_data, file_path):
    with open(file_path, 'a') as file:
        file.write(json.dumps(json_data, indent=4) + '\n')

def delete_file(file_path):
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 删除文件
        os.remove(file_path)
        print(f"文件 {file_path} 已被删除。")
    else:
        print(f"文件 {file_path} 不存在。")