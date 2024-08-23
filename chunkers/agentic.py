from typing import List
from pydantic import BaseModel

from llm import OpenAI
from chunkers import BaseChunker

class Sentences(BaseModel):
    sentences: List[str]

SYSTEM_PROMPT = """You are a Agent who helps spliting the given content into chunks of meanigful sentences. Each chunk will have a maximum 500 characters."""

class AgenticChunker(BaseChunker):
    def __init__(self, llm_client=OpenAI(model="gpt-4o-mini")):
        self.llm_client = llm_client
    
    def get_chunks(self, text):
        result = self.llm_client.chat_parsed(messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ], response_format=Sentences)
        return result.sentences