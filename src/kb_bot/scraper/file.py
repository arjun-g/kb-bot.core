import uuid
from llama_index.core import SimpleDirectoryReader

from ..chunkers import BasicChunker
from ..embedding import OpenAIEmbedClient

class FileScraper:
    def __init__(
            self,
            files=[],
            chunker=BasicChunker(),
            embedding_client=OpenAIEmbedClient(),
            db_provder=None,
            group=None
    ):
        file_metadata = lambda x: {"filename": x}
        self.reader = SimpleDirectoryReader(input_files=files, file_metadata=file_metadata)
        self.chunker = chunker
        self.embedding_client = embedding_client
        self.db_provider = db_provder
        self.group = group

    def scrape(self):
        docs = self.reader.load_data()
        for doc in docs:
            chunks = self.chunker.get_chunks(doc.text)
            for chunk in chunks:
                if(bool(chunk.strip())):
                    self.db_provider.insert({
                        "id": str(uuid.uuid1()),
                        "title": doc.metadata.get("filename"),
                        "content": chunk,
                        "ref": doc.metadata.get("filename"),
                        "embedding": self.embedding_client.embed(str(chunk)),
                        "type": "file",
                        "group": self.group
                    })
