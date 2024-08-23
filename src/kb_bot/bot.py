import json

class KBBot:

    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_kb",
                "description": "Search for articles in the knowledge base. The search will happen with a vector representation of the query.",
                "parameters": {
                    "type": "object",
                    "properties":{
                        "query": {
                            "type": "string",
                            "description": "The query to search for. The vector representation of the query will be used to search for similar articles in the knowledge base."
                        }
                    },
                    "required": ["query"]
                },
            }
        }
    ]    

    def __init__(
        self,
        db_provider,
        embedding_client,
        llm_client,
        group=None,
        tasks_prompt="",
        history=[]
    ):
        self.db_provider = db_provider
        self.embedding_client = embedding_client
        self.llm_client = llm_client
        self.group = group
        self.tasks_prompt = tasks_prompt
        self.history = history
        
    def system_prompt(self):
        return f"""
        You are a assistant helping people to find information in a knowledge base. You have access to a database of knowledge base articles.
        Tasks:
        - Search for articles in the knowledge base.
        {self.tasks_prompt}
        Important:
        - You can search the articles by typing 'search_kb'.
        - You will answer only the questions related to the knowledge base articles.
        - If you don't know the answer, politely ask ofr more information if needed, or say you don't know.

        """
        
    def search_kb(
        self,
        query
    ):
        vector = self.embedding_client.embed(query)
        results = self.db_provider.search(vector, group=self.group)
        return results
    
    def chat(
        self,
        message
    ):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt()
            },
            *self.history,
            {
                "role": "user",
                "content": message
            }
        ]
        response = self.llm_client.chat(messages=messages, tools=self.tools)
        if(response.choices[0].message.function_call):
            tool_call_responses = []
            for tool_call in response.choices[0].message.tool_calls:
                kbs = self.search_kb(json.loads(tool_call["function"]["arguments"])["query"])
                tool_call_responses.append({
                    "role": "tool",
                    "content": json.dumps({
                        "kbs": kbs
                    }),
                    "tool_call_id": tool_call["id"]
                })
            response = self.llm_client.chat(messages=[*messages, *tool_call_responses], tools=self.tools)
        return response.choices[0].message