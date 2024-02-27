# data-analysis

## 如果是第一次使用，请先创建虚拟环境，然后安装依赖

## 本地开发环境

1. 创建虚拟环境
```shell
python3 -m venv venv
```
2. 激活虚拟环境
```shell
source venv/bin/activate
```
3. 安装依赖
```shell
pip3 install -r requirements.txt
```

## 运行

1. 环境变量配置
新建.env文件，参考.env.example
配置OPENAI_API_KEY  
OUTPUT_DIR可以不变

2. 运行
```shell
python3 main/index.py
```

## 运行结果

- /output/source_table.json  
    从source.sql提取出来的表结构
- /output/orginal_entities.json  
    gpt直接生成的实体，缺少字段
- /output/entities.json
    补全字段后的实体



## 如果更新了依赖记得更新requirements.txt

```shell
pip3 freeze > requirements.txt
```