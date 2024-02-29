from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.output_parsers.json import SimpleJsonOutputParser
from dotenv import load_dotenv

load_dotenv()


class ChatModel:
    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        prompt: str = "You are a helpful assistant",
        is_json_output: bool = False,
    ):
        llm = ChatOpenAI(temperature=0, model=model)
        self.llm = llm
        self.prompt = prompt
        self.is_json_output = is_json_output
        if self.is_json_output:
            self.chain = llm | SimpleJsonOutputParser()
        else:
            self.chain = llm

    def invoke(self, message: str):
        messages = [SystemMessage(content=self.prompt), HumanMessage(content=message)]
        return self.chain.invoke(messages)
