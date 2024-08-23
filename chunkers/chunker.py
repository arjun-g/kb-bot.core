from typing import List


class BaseChunker:
    def get_chunks(self, text) -> List[str]:
        pass