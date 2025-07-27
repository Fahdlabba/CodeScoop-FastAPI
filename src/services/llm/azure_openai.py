from .llm import LLM
from openai import AzureOpenAI
from dotenv import load_dotenv
from src.services.tools.fetch_file_content import fetch_content

from typing import List, Optional
import os
from loguru import logger

load_dotenv()
import json

class AzureOpenAIService(LLM):
    _client= AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_KEY"),
        api_version=os.getenv("api_version")
    )
    def __init__(self,code_tree:List[dict[str, List[str]]])-> None:
        self.chat_history = [{"role": "system", "content": self.load_prompt()},
                             {"role": "user", "content": f"{code_tree}"}]
        self.tool_schema = [
                {
                "type": "function",
                "function": {
                    "name": "fetch_content",
                    "description": "You can use this tool to fetch the content of a Python file from the repository when you need to access its code.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The location of the file to fetch",
                            }
                        },
                        "required": ["file_path"],
                    },
                },
            }]
        self.tools={"fetch_content": fetch_content}

    def load_prompt(self):
        with open("src/prompt/system_prompt_template.txt", "r") as file:
            return file.read()
        

    def format_message(self, role:str,content:str,tool_id:Optional[any]) -> List[dict]:
        if tool_id:
            return self.chat_history.append({"role": role, "content": content, "tool_call_id": tool_id})
        return self.chat_history.append({"role": role, "content": content})
    
    def get_response(self,path) -> str:

    
        message = self.chat_history
        try : 
            response = AzureOpenAIService._client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                messages=message,
                temperature=0.7,
                tools=self.tool_schema,
                tool_choice="auto",
            )
            logger.info("Response received from Azure OpenAI")
            response_content = response.choices[0].content
            

            if response_content.tool_calls:
                logger.info(f"Tool calls detected: {response_content.tool_calls}")
                self.chat_history.append(response_content)
                for tool_call in response_content.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    if tool_name in self.tools:
                        tool_2_call = self.tools[tool_name]
                        tool_response = tool_2_call(os.path.join(path, tool_args.get("file_path", "")))
                        self.format_message("tool", tool_response, tool_id=tool_call.id)
                        
            logger.info("Finalizing response")

            final_response = AzureOpenAIService._client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                messages=self.chat_history,
                temperature=0.7,
                tools=self.tool_schema,
                tool_choice="auto",
              
            )

            return final_response.choices[0].content
        except Exception as e:
            logger.error(f"Error in AzureOpenAI get_response: {e}")
            return f"An error occurred while processing your request: {e}"


        


           
