import json
from src.config.settings import get_settings
from src.services.tools.fetch_file_content import fetch_content
from groq import Groq
from .llm import LLM
from typing import List,Optional
from loguru import logger

import os


class GroqLLM(LLM):
    __groq_client:Groq = Groq(api_key=get_settings().GROQ_API_KEY)

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
                                "description": "The location of the file to fetch , use absolute path",
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

    def get_response(self) -> str:

        message = self.chat_history
        try : 
            response = GroqLLM.__groq_client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct",
                messages=message,
                temperature=0.7,
                tools=self.tool_schema,
                tool_choice="auto",
            )
            logger.info("Response received from Groq LLM")
            response_content = response.choices[0].message
            

            if response_content.tool_calls:
                logger.info(f"Tool calls detected: {response_content.tool_calls}")
                self.chat_history.append(response_content)
                for tool_call in response_content.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    if tool_name in self.tools:
                        tool_2_call = self.tools[tool_name]
                        tool_response = tool_2_call(tool_args.get("file_path", ""))
                        logger.info(f"Tool response: {tool_response}")
                        self.format_message("tool", tool_response, tool_id=tool_call.id)
                        
            logger.info("Finalizing response")

            final_response = GroqLLM.__groq_client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct",
                messages=self.chat_history,
                temperature=0.7,
                tools=self.tool_schema,
                tool_choice="auto",
              
            )

            return final_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in GroqLLM get_response: {e}")
            return f"An error occurred while processing your request: {e}"


if __name__ == "__main__":
    llm = GroqLLM()
    response = llm.get_response("What is the purpose of this code?")
    print(response)
        


