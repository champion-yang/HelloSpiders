# coding=utf-8
"""
@auth: xiaobei
@date: 2020/12/27
@desc:
"""
from abc import ABC

import scrapy
from scrapy import Request, Spider, FormRequest
import nest_asyncio
import asyncio
from playwright import async_playwright
from pyquery import PyQuery as pq

nest_asyncio.apply()


class JueJinSpider(Spider):
    name = 'juejin'
    allowed_domains = ['juejin.cn/']
    start_urls = ['https://api.juejin.cn/content_api/v1/article/query_list']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Referer': 'https://juejin.cn/',
        'Content-Type': 'application/json'
    }

    def start_requests(self):
        yield FormRequest(
            self.start_urls[0],
            callback=self.parse,
            formdata={
                "user_id": "1574156384091320",
                "sort_type": str(1),
                "cursor": "0",
            }
        )

    def parse(self, response, **kwargs):
        print(response.json())

