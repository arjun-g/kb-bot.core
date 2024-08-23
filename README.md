# kb-bot.core

The core library of kb-bot. This handles indexing of content, and chatting with the bot.

## Getting Started

```bash
pip install kb-bot.core
```

## Preparing the KB

```python
import os
from kb_bot import KBBot
from kb_bot.scraper import WebScraper
from kb_bot.db import TiDBProvider
from kb_bot.chunkers import SemanticChunker
from kb_bot.embedding import OpenAIEmbedClient
from kb_bot.llm import OpenAI

# Configure env variables TIDB_DATABASE, TIDB_USERNAME, TIDB_PASSWORD, TIDB_HOST, TIDB_PORT
tidb = TiDBProvider()
tidb.connect()

embed_client = OpenAIEmbedClient(
    api_key=os.environ.get('OPENAI_API_KEY')
)

scraper = WebScraper(
    urls=["https://www.pingcap.com/blog/"],
    follow_links=True,
    restrict_navigation_css=".tmpl-archive.tmpl-archive-blog",
    restrict_css=".tmpl-single-post__content",
    ignore_css=".tmpl-archive-sidebar",
    chunker=SemanticChunker(
        embedding_client=embed_client
    ),
    db_provider=tidb,
    group="<user user id or project id according to your need>",
    embedding_client=embed_client
)

scraper.crawl()
```

## Chat with the bot

```python
bot = KBBot(
    db_provider=tidb,
    embedding_client=embed_client,
    group="new-user-id",
    llm_client=OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    ),
    history=[],
    tasks_prompt="<Additional instructions to bot>"
)

response = bot.chat(message="what are the benefits of vector search ?")
print(response)
```

## TODO
- Add support for multiple llm(s)
- Implement Agentic Chunker
- Add test cases
