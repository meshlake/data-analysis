from utils.util import read_json, write_json_to_file
from output_manage import get_output_path
import os
from llm import ChatModel


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
                Step 4: Return these questions in the sample json format

                sample json format:
                [
                    "What is the average value of the number of people in the population?",
                    "What is the maximum value of the number of people in the population?",
                    "What is the minimum value of the number of people in the population?",
                    "What is the standard deviation of the number of people in the population?",
                ]
            """,
        is_json_output=True,
    )

    questions = llm.invoke(f"{entities}\n{metrics}")
    return questions


if __name__ == "__main__":
    questions = generate_question()
    write_json_to_file(questions, "question/student.json")
