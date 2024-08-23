from typing import List
from pydantic import BaseModel

from ..llm import OpenAI
from .chunker import BaseChunker

class Chunks(BaseModel):
    chunks: List[str]
class AgenticChunker(BaseChunker):
    def __init__(self, llm_client):
        self.llm_client = llm_client or OpenAI(model="gpt-4o-mini")
    
    def get_chunks(self, text):
        # To be implemented
        pass