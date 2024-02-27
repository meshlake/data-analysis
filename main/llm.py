from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview")
