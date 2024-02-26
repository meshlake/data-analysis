import json


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
