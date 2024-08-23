from llama_index.embeddings.openai import OpenAIEmbedding

class OpenAIEmbedClient(OpenAIEmbedding):

    def embed(self, text):
        return self.embed(text)