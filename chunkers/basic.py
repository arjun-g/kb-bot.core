from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

from chunkers.chunker import BaseChunker

class BasicChunker(BaseChunker):
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.node_parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    def get_chunks(self, text):
        nodes = self.node_parser.get_nodes_from_documents([Document(text=text)])
        chunks = []
        for node in nodes:
            chunks.append(node.get_content())
        return chunks