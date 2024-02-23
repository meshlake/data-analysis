dev.json 为spider数据集中所有的question和sql的集合

所以针对单个db的数据，可以执行对应文件下的`filter_data.py`文件，生成对应的`sql.json`文件

例如生成`student_transcripts_tracking`数据集的`sql.json`，在当前目录下执行如下命令：

```shell
python3 student_transcripts_tracking/filter_data.py
```