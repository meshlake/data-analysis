import os
import logging
from utils.util import read_json, read_file, write_json_to_file, delete_file
from output_manage import get_output_path, get_vector_store_path
from tqdm import tqdm
from functools import reduce
from operator import add
from llm import ChatModel
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


class Entity:

    original_storage = "orginal_entities.json"
    storage = "entities.json"
    vector_store_path = get_vector_store_path()

    def __init__(self):
        prompt = """
            You are an expert in the field of data analysis, proficient in datamesh theory and SQL syntax, 
            and know that data entities are divided according to business meanings and can be formed by joining one table or multiple tables. 
            Next, I will give you a table schema of the data field and some sql in this data field. 
            Please create data entities according to the table given to you, and give the business meaning of these entities, source table and table join sql.
            Just return the json structure like the example.

            For example:
            [
                {
                    "name": "address",
                    "businessSemantics": "Represents the different addresses where students might reside or have lived.",
                    "sourceTable": ["Addresses"],
                    "joinSql": "SELECT * FROM Addresses",
                },
                {
                    "name": "Student Enrolment Courses",
                    "businessSemantics": "Links student enrollments to specific courses.",
                    "sourceTable": ["Student_Enrolment_Courses","Courses"],
                    "joinSql": "SELECT * FROM Student_Enrolment_Courses JOIN Courses ON Student_Enrolment_Courses.course_id = Courses.course_id",
                }
            ]
        """
        self.builder = ChatModel(prompt=prompt, is_json_output=True)

    def __load_requirements(self):
        """filter sql data

        return:
            list: [{"question": "xxx", "query": "xxx"}]
        """
        sql_path = os.environ["sql"]
        sql_data = read_json(sql_path)
        filter_sql = [
            {"question": item["question"], "query": item["query"]} for item in sql_data
        ]
        schema = read_file(os.environ["schema"])
        return (filter_sql, schema)

    def __find_source_table(self, table_names: list[str], source_tables: list):
        return [
            source_table
            for source_table in source_tables
            if source_table["name"] in table_names
        ]

    def __build_original_entities(self):
        logging.info("start to build original entities...")

        (filter_sql, schema) = self.__load_requirements()

        sql = filter_sql.__str__()
        original_entities = self.builder.invoke(f"```{schema}```\n```{sql}```")

        logging.info("build original entities success")

        original_storage_file = get_output_path(self.original_storage)
        delete_file(original_storage_file)

        write_json_to_file(original_entities, original_storage_file)

        return original_entities

    def build_entities(self, force=False):
        if not force and os.path.exists(get_output_path(self.original_storage)):
            logging.info("Orginal metrics already exists, skip building")
            original_entities = read_json(get_output_path(self.original_storage))
        else:
            original_entities = self.__build_original_entities()
        
        source_tables = read_json(get_output_path("source_table.json"))
        entity_file = get_output_path(self.storage)
        delete_file(entity_file)
        entities = []
        try:
            for entity in tqdm(original_entities):
                entity_source_table_names = entity["sourceTable"]
                entity_source_tables = self.__find_source_table(
                    entity_source_table_names, source_tables
                )
                entity["fields"] = reduce(
                    add,
                    [source_table["fields"] for source_table in entity_source_tables],
                )
                entity["category"] = "ENTITY"
                entities.append(entity)
            write_json_to_file(entities, entity_file)
        except Exception as e:
            logging.error(f"build entity failed: {e}")
            write_json_to_file(entities, entity_file)

    def build_vector_store(self, force=False):

        if not force and os.path.exists(get_output_path(self.storage)):
            loader = JSONLoader(
                file_path=get_output_path(self.storage),
                jq_schema=".[]",
                text_content=False,
            )
            entities = loader.load()

            def add_metadata(entity):
                entity.metadata["category"] = "ENTITY"
                return entity

            entities = [add_metadata(entity) for entity in entities]
        else:
            logging.warning("entities not found, skip building vector store")

        Chroma.from_documents(
            entities,
            OpenAIEmbeddings(),
            persist_directory=self.vector_store_path,
            collection_name="entities",
        )

    @classmethod
    def search_by_natural_language(cls, query: str = ""):
        vector_store = Chroma(
            persist_directory=cls.vector_store_path,
            embedding_function=OpenAIEmbeddings(),
            collection_name="entities",
        )
        docs = vector_store.similarity_search(query)
        return docs

    @classmethod
    def search_by_source_tables(cls, source_tables: list = []):
        entities = read_json(get_output_path(cls.storage))
        return [
            entity
            for entity in entities
            if all(table in entity["sourceTable"] for table in source_tables)
            or set(entity["sourceTable"]) == set(source_tables)
        ]
