from pydantic import BaseModel,Field
from loguru import logger




class ToolsCallSchema(BaseModel):
    file_path: str = Field(..., description="Path to the file from which to fetch content.")

def fetch_content(file_path: str) -> str:
    """Return the content of the file at the given path.
    
    Args:
        file_path (str): The path to the file from which to fetch content e.g. "src/data/example.py".
    """
    try:
        logger.info(f"Fetching content from file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while fetching the file content: {e}")

