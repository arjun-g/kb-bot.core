import openai

class OpenAI:
    def __init__(self, model="gpt-4o-mini"):
        self.client = openai.Client()
        self.model = model

    def chat(self, messages, response_format=None):
        return self.client.beta.chat.completions.parse(
            messages=messages,
            model=self.model,
            response_format=response_format
        )
    
    def chat_parsed(self, messages, model="gpt-4o-mini", response_format=None):
        return self.chat(messages, model, response_format).choices[0].message.parsed