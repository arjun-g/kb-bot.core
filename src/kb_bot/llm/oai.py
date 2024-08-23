import openai

class OpenAI:
    def __init__(self, model="gpt-4o-mini", api_key=None):
        self.client = openai.Client(
            api_key=api_key
        )
        self.model = model

    def chat(self, messages, tools, response_format=None):
        return self.client.beta.chat.completions.parse(
            messages=messages,
            model=self.model,
            response_format=response_format,
            tools=tools
        )
    
    def chat_parsed(self, messages, response_format=None):
        return self.chat(messages, response_format).choices[0].message.parsed