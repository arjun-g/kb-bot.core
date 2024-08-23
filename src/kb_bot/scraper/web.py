import crochet

from chunkers import BasicChunker
crochet.setup()

import uuid
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from ..embedding import OpenAIEmbedClient

class WebSpider(CrawlSpider):
    name = "web-scraper"
    
    crawled_urls = []
    
    def __init__(
        self,
        urls=None,
        follow_links=True,
        restrict_navigation_css=None,
        restrict_css=None,
        ignore_css=None,
        *args,
        **kwargs
    ):
        print("Initializing ContentSpider")
        self.rules = (
            Rule(LinkExtractor(
                restrict_css=restrict_navigation_css,
                unique=True
            ), callback='parse_page', follow=follow_links),
        )
        super(WebSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls
        self.restrict_css = restrict_css
        self.ignore_css = ignore_css
    
    def parse_page(self, response):
        print("Crawling 1:", response.url)
        soup = BeautifulSoup(response.body, 'html.parser')
        try:
            if(self.ignore_css):
                for element in soup.select(selector=self.ignore_css):
                    element.decompose()
            if(self.restrict_css):
                content = " ".join([p.get_text() for p in soup.select(selector=self.restrict_css)])
            else:
                content = soup.get_text()
            yield {
                "content": content,
                "url": response.url,
                "title": response.css('title::text').get()
            }
        except Exception as e: print(e)
        
        
        
class WebScraper():
    
    MAX_LINK_FOLLOW = 1000
    
    def __init__(
        self,
        urls=None,
        follow_links=True,
        restrict_navigation_css=None,
        restrict_css=None,
        ignore_css=None,
        db_provider=None,
        embedding_client=OpenAIEmbedClient(),
        chunker=BasicChunker(),
        group=None
    ):
        self.crawl_runner = CrawlerRunner()
        self.urls = urls
        self.follow_links = follow_links
        self.restrict_navigation_css = restrict_navigation_css
        self.restrict_css = restrict_css
        self.ignore_css = ignore_css
        self.db_provider = db_provider
        self.chunker = chunker
        self.embedding_client = embedding_client
        self.group = group
        
    @crochet.run_in_reactor
    def crawl(self):
        print("Crawling 2:", self.urls)
        dispatcher.connect(self._crawler_result, signal=signals.item_scraped)
        try:
            self.eventual = self.crawl_runner.crawl(
                WebSpider,
                urls=self.urls,
                follow_links=self.follow_links,
                restrict_navigation_css=self.restrict_navigation_css,
                restrict_css=self.restrict_css,
                ignore_css=self.ignore_css
            )
        except Exception as e: print(e)
        
    def cancel(self):
        self.eventual.cancel()
    
    def _crawler_result(self, item, response, spider):
        for chunk in self.chunker.get_chunks(item["content"]):
            self.db_provider.insert({
                "id": str(uuid.uuid1()),
                "title": item["title"],
                "content": chunk,
                "ref": item["url"],
                "embedding": self.embedding_client.embed(chunk),
                "type": "web",
                "group": self.group
            })
