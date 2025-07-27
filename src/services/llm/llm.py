from abc import ABC
from typing import List


class LLM(ABC):
    def __init__(self,code_tree) -> None:
        pass


    def get_response(self,
        message: List[str],    
        temperature: float = 0.5,
        stream: bool = False,
        max_new_tokens: int = 512,
        tools: List[dict] = None,
        ) -> str:
        pass