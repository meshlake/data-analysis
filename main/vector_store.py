import os
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from langchain_community.vectorstores import Chroma


class VectorStore:
    def __init__(self, collection_name: str):
        path = self.__get_vector_store_path()
        self.persistent_client = chromadb.PersistentClient(path=path)
        openai_ef = embedding_functions.OpenAIEmbeddingFunction()
        self.collection = self.persistent_client.get_or_create_collection(
            collection_name, embedding_function=openai_ef
        )
        Chroma(collection_name=self.collection_name)

    def __get_vector_store_path(self):
        current_dir = os.path.dirname(__file__)
        DEFAULT_OUTPUT = "chroma_db"
        return os.path.abspath(os.path.join(current_dir, f"./{DEFAULT_OUTPUT}"))

    def similarity_search(self, query: str = ""):
        return self.collection.query(query_texts=[query], n_results=10)
