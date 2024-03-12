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
   新建.env 文件，参考.env.example
   配置 OPENAI_API_KEY  
   OUTPUT_DIR 可以不变

2. 准备数据
   将 schema.sql 放到/data/default 目录下
   schema.sql 是数据库的表结构
   例如
   CREATE TABLE `Breeds` (
   `breed_code` VARCHAR(10) PRIMARY KEY ,
   `breed_name` VARCHAR(80)
   );
   CREATE TABLE `Charges` (
   `charge_id` INTEGER PRIMARY KEY ,
   `charge_type` VARCHAR(10),
   `charge_amount` DECIMAL(19,4)
   );

   将 sql.json 放到/data/default 目录下
   sql.json 是问题和 sql 的组合，辅助数据分析
   例如
   [{
   "query": "SELECT state FROM Owners INTERSECT SELECT state FROM Professionals",
   "question": "Which states have both owners and professionals living there?",
   }]
   请按照样例结构生成

3. 运行

```shell
# 构建数据分析资源，请耐心等待构建完成
python3 main/build.py

# 开启命令行对话框，输入问题，获取答案 输入q退出
python3 main/start.py
```

## 运行结果

- /output/source_table.json  
   从 source.sql 提取出来的表结构
- /output/orginal_entities.json  
   gpt 直接生成的实体，缺少字段
- /output/entities.json
  补全字段后的实体

## 如果更新了依赖记得更新 requirements.txt

```shell
pip3 freeze > requirements.txt
```
