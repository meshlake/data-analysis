import os


def get_output_path(file_name: str):
    current_dir = os.path.dirname(__file__)
    DEFAULT_OUTPUT = "output"
    output_dir = (
        os.environ["OUTPUT_DIR"] if os.environ["OUTPUT_DIR"] else DEFAULT_OUTPUT
    )
    return os.path.abspath(os.path.join(current_dir, f"./{output_dir}/{file_name}"))
