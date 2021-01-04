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


class TouTiaoSpider(Spider):
    name = 'toutiao'
    allowed_domains = ['www.toutiao.com']
    start_urls = ['https://www.toutiao.com/c/user/token/MS4wLjABAAAAigrrKo-3rjLpxaH4Go3BrZRqHTIhLW3e30QjfFXgzNQ/']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Referer': 'https://www.toutiao.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response, **kwargs):
        print(222)
        print(response.url)
        async def playweight_demo():
            async with async_playwright() as p:
                width, height = 1366, 768
                browser = await p.chromium.launch(headless=False, devtools=True, args=['--disable-infobars',
                                                                                      f'--window-size={width},{height}'])
                page = await browser.newPage()
                await page.setExtraHTTPHeaders(headers=self.headers)
                await page.setViewportSize(width, height)
                await page.goto(response.url)

                await page.waitForSelector(selector='feed-list', timeout=5000, state='attached')

                await browser.close()

        asyncio.get_event_loop().run_until_complete(playweight_demo())
