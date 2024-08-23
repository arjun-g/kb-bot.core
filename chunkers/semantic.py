from llama_index.core import Document
from llama_index.core.node_parser import (
    SemanticSplitterNodeParser,
)

from chunkers import BaseChunker
from embedding import OpenAIEmbedClient

class SemanticChunker(BaseChunker):
    def __init__(self, buffer_size=1, breakpoint_percentile_threshold=95):
        embed_model = OpenAIEmbedClient()
        self.node_parser = SemanticSplitterNodeParser(
            buffer_size=buffer_size, breakpoint_percentile_threshold=breakpoint_percentile_threshold, embed_model=embed_model
        )
    
    def get_chunks(self, text):
        nodes = self.node_parser.get_nodes_from_documents([Document(text=text)])
        chunks = []
        for node in nodes:
            chunks.append(node.get_content())
        return chunks