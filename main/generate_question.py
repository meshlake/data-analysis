from utils.util import read_json, write_json_to_file
from output_manage import get_output_path
import os
from llm import ChatModel
import requests
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyDyXmy7P5K_IedOWTCL_9e16H16921slVI")

# Set up the model
# generation_config = {
#     "temperature": 0.9,
#     "top_p": 1,
#     "top_k": 1,
#     "max_output_tokens": 2048,
# }

# safety_settings = [
#     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
#     {
#         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
#     {
#         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#         "threshold": "BLOCK_MEDIUM_AND_ABOVE",
#     },
# ]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro"
)


def filter_data(type: str = "student"):
    if type == "student":
        os.environ["OUTPUT_DIR"] = "output"
    else:
        os.environ["OUTPUT_DIR"] = "output1"
    entities_path = get_output_path("entities.json")
    entities = read_json(entities_path)
    metrics_path = get_output_path("metrics.json")
    metrics = read_json(metrics_path)

    def simple_field(entity):
        entity["fields"] = [
            {"name": field["name"], "description": field["description"]}
            for field in entity["fields"]
        ]
        return entity

    entity = [simple_field(entity) for entity in entities]

    return entity, metrics


def generate_question():
    entities, metrics = filter_data()

    llm = ChatModel(
        prompt="""
                You are an expert in datamesh. 
                You need to generate some verification questions based on entity and indicator data to verify the ability of other large models to generate SQL. 
                Please follow the steps below to generate
            
                Step 1: Understand entity and metric data
                Step 2: Based on the data, generate 10 questions about statistical indicators of these data.
                        The problem needs to be complex enough to include multiple dimensions and multiple indicators. 
                        Indicators should include derived indicators.
                        Do not generate questions that are already in the data.
                Step 3: Check these questions to see if they meet the requirements
                Step 4: Generate sql for these questions
                Step 5: Return these questions and sqls in the sample json format

                sample json format:
                [   
                    {
                        "question": "What is the average value of the number of people in the population?",
                        "query": "SELECT AVG(population) FROM population"
                    },
                    {
                        "question": "What is the average value of the number of people in the population?",
                        "query": "SELECT AVG(population) FROM population"
                    }
                ]
            """,
        is_json_output=True,
    )

    questions = llm.invoke(f"{entities}\n{metrics}")
    return questions


if __name__ == "__main__":
    # questions = generate_question()
    # write_json_to_file(questions, "question/student.json")
    entities, metrics = filter_data()
    print(entities)
    print("====================================")
    print(metrics)
    # convo = model.start_chat(
    #     history=[
    #         {
    #             "role": "user",
    #             "parts": [
    #                 """
    #             You are an expert in datamesh. 
    #             You need to generate some verification questions based on entity and indicator data to verify the ability of other large models to generate SQL. 
    #             Please follow the steps below to generate
            
    #             Step 1: Understand entity and metric data
    #             Step 2: Based on the data, generate 10 questions about statistical indicators of these data.
    #                     The problem needs to be complex enough to include multiple dimensions and multiple indicators. 
    #                     Indicators should include derived indicators.
    #                     Do not generate questions that are already in the data.
    #             Step 3: Check these questions to see if they meet the requirements
    #             Step 4: Generate sql for these questions
    #             Step 5: Return these questions and sqls in the sample json format

    #             sample json format:
    #             [   
    #                 {
    #                     "question": "What is the average value of the number of people in the population?",
    #                     "query": "SELECT AVG(population) FROM population"
    #                 },
    #                 {
    #                     "question": "What is the average value of the number of people in the population?",
    #                     "query": "SELECT AVG(population) FROM population"
    #                 }
    #             ]
    #         """
    #             ],
    #         }
    #     ]
    # )

    # convo.send_message(f"entities: {entities}\n metrics: {metrics}")
    # print(convo.last.text)

    # convo = model.start_chat(
    #     history=[]
    # )

    # response = convo.send_message("你好")
    # print(response.text)

