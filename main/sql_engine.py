from langchain_community.vectorstores import Chroma
from llm import ChatModel
from output_manage import get_vector_store_path
from langchain_openai import OpenAIEmbeddings


class SqlEngine:
    vector_store_path = get_vector_store_path()

    def __init__(self):

        prompt = """
            You are an expert in data analysis and SQL syntax, and are good at datamesh theory.
            I'll give you some structure for business entities, metrics, and dimensions.
            Please follow the steps below to generate sql statements based on the user's questions and these structural information.
            Step 1: Understand the user’s problem
            Step 2: Understand the structural information given to you
            Step 3: Generate sql
            Step 4: Return the question and sql in the sample json format

            For example:
            input:
            ```
            question: "How many courses in total are listed?"

            entities: {
                "name": "Courses",
                "businessSemantics": "Represents the academic courses offered by an educational institution.",
                "sourceTable": [
                    "Courses"
                ],
                "joinSql": "SELECT * FROM Courses",
                "fields": [
                    {
                        "name": "course_id",
                        "description": "course id",
                        "dataType": "INTEGER",
                        "nullable": "False",
                        "primaryKey": "True",
                        "foreignKey": "False"
                    },
                    {
                        "name": "course_name",
                        "description": "course name",
                        "type": "VARCHAR(255)",
                        "nullable": "False",
                        "primaryKey": "False",
                        "foreignKey": "False"
                    },
                    {
                        "name": "course_description",
                        "description": "course description",
                        "type": "VARCHAR(255)",
                        "nullable": "False",
                        "primaryKey": "False",
                        "foreignKey": "False"
                    },
                    {
                        "name": "other_details",
                        "description": "other details",
                        "type": "VARCHAR(255)",
                        "nullable": "True",
                        "primaryKey": "False",
                        "foreignKey": "False"
                    }
                ]
            }

            metrics: {
                "name": "total_courses_count",
                "businessSemantics": "total number of courses listed",
                "sourceTable": [
                    "Courses"
                ],
                "aggregation": "COUNT",
                "field": "*",
                "dataType": "INTEGER",
                "original": {
                    "question": "How many courses in total are listed?",
                    "query": "SELECT count(*) FROM Courses"
                },
                "entities": [
                    "Courses"
                ]
            }
            ```

            output:
            ```
            {
                "question": "How many courses in total are listed?",
                "query": "SELECT count(*) FROM Courses"
            }
            ```
        """

        self.llm = ChatModel(prompt=prompt, is_json_output=True)

        self.entity_searcher = Chroma(
            persist_directory=self.vector_store_path,
            embedding_function=OpenAIEmbeddings(),
            collection_name="entities",
        )

        self.metric_searcher = Chroma(
            persist_directory=self.vector_store_path,
            embedding_function=OpenAIEmbeddings(),
            collection_name="metrics",
        )

    def invoke(self, question: str):
        entities = self.entity_searcher.similarity_search(query=question)
        metrics = self.metric_searcher.similarity_search(query=question)

        return self.llm.invoke(
            f"```question:{question}\nentity:{entities}\nmetric:{metrics}```"
        )
