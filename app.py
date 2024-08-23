

# import dotenv
# dotenv.load_dotenv()

# import time
# import uuid
# from pathlib import Path
# from flask import Flask, request, jsonify
# from scrapy import signals
# from scrapy.crawler import CrawlerRunner
# from scrapy.signalmanager import dispatcher
# from libs.webscraper import ContentSpider

# app = Flask(__name__)

# crawl_runner = CrawlerRunner()

# @crochet.run_in_reactor
# def crawl(urls, restrict_navigation_css=None, restrict_css=None, ignore_css=None):
#     dispatcher.connect(_crawler_result, signal=signals.item_scraped)
#     eventual = crawl_runner.crawl(ContentSpider, urls=urls, restrict_navigation_css=restrict_navigation_css, restrict_css=restrict_css, ignore_css=ignore_css,follow_links=False)
#     return eventual

# def _crawler_result(item, response, spider):
#     print('Got item:', item["url"])
#     # print('Got item:', item["content"])
#     # Path(f"html/{str(uuid.uuid1())}.html").write_text(item["content"])
    
# eventual = crawl(["https://www.pingcap.com/blog/"], ".tmpl-archive-posts-container,.tmpl-single-post__content", ".tmpl-archive-sidebar")
# time.sleep(10)
# print("cancelling")
# eventual.cancel()
# time.sleep(10)


import dotenv
dotenv.load_dotenv()

import time
from scraper.web import WebScraper
from db.tidb import TiDBProvider

db_provider = TiDBProvider()

db_provider.connect()

scraper = WebScraper(
    urls=["https://www.pingcap.com/blog/"],
    restrict_css=".tmpl-archive-posts-container,.tmpl-single-post__content",
    restrict_navigation_css=".tmpl-archive-posts-container,.tmpl-single-post__content",
    follow_links=True,
    db_provider=db_provider
)

scraper.crawl()
time.sleep(10)