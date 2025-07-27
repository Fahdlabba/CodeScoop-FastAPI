from src.services.tools.fetch_file_content import fetch_content
from dotenv import load_dotenv
from google.genai import types
from loguru import logger
from google import genai
from typing import List,Optional
from .llm import LLM
import os
load_dotenv()



class GeminiLLM(LLM):
    _client=genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )
    def __init__(self,code_tree:any,graph:Optional[any]=None)-> None:
        self.chat_history = [types.Content(
            role='user',
            parts=[
                types.Part(
                    text=f"Files Code :  {code_tree} \n\n Call Graph {graph}" if graph else f"Code Tree: {code_tree}"
                    )]
            )]

    def load_prompt(self,system_prompt):
        with open(f"src/prompt/{system_prompt}.txt", "r") as file:
            return file.read()
        
    def generate_response(self,task_type="readme") -> str:
        try:
            response = GeminiLLM._client.models.generate_content(
                model="gemini-2.5-flash",
                contents=self.chat_history,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=0,
                    ),
                    tools=[fetch_content if task_type == "readme" else types.Tool(code_execution=types.ToolCodeExecution)],
                    system_instruction=[
                    types.Part.from_text(text=self.load_prompt("system_prompt_template") if task_type == "readme" else self.load_prompt("code_review")),
                ],
                    response_mime_type="text/plain"
                    
                )
            )
         
            return response.text
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise Exception(f"An error occurred while generating the response: {e}")
        