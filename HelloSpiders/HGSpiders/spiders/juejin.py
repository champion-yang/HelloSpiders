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
from HelloSpiders.HGSpiders.items import *
import logging
import requests

nest_asyncio.apply()


class JueJinSpider(Spider):
    name = 'juejin'
    allowed_domains = ['api.juejin.cn']
    start_urls = ['https://api.juejin.cn/content_api/v1/article/query_list']
    user_api = "https://api.juejin.cn/user_api/v1/user/get?aid=2608&user_id=1574156384091320&not_self=1"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.payload = None
        self.sub_domains = "https://juejin.cn/post/"
        self.cursor_range = [0, 10, 20, 30]
        self.post_article_count = 0

    def start_requests(self):
        yield Request(
            self.user_api,
            headers=self.headers,
            callback=self.per_parse
        )

    def per_parse(self, response, **kwargs):
        blogger_json = response.json()
        if blogger_json.get('err_msg') == 'success':
            _item = HgspidersItem()
            _item['source_name'] = '掘金'
            _item['item_type'] = 2
            _item['blogger_name'] = blogger_json['data']['user_name']
            _item['followee_count'] = blogger_json['data']['followee_count']
            _item['follower_count'] = blogger_json['data']['follower_count']
            _item['post_article_count'] = blogger_json['data']['post_article_count']
            _item['got_digg_count'] = blogger_json['data']['got_digg_count']
            _item['got_view_count'] = blogger_json['data']['got_view_count']

            yield _item

        self.post_article_count = blogger_json['data']['post_article_count'] if str(blogger_json['data']['post_article_count']).endswith('0') \
            else blogger_json['data']['post_article_count'] + 10

        for i in [i for i in range(0, self.post_article_count, 10)]:
            self.payload = '{"user_id": "1574156384091320", "sort_type": 2, ' + f'"cursor": "{i}"' + "}"

            yield Request(
                self.start_urls[0],
                headers=self.headers,
                callback=self.parse,
                method='POST',
                body=self.payload,
            )

    def parse(self, response, **kwargs):
        response_json = response.json()
        if response_json.get('err_msg') == 'success' and response_json['has_more']:
            for d in response_json['data']:
                hg_item = HgspidersItem()
                hg_item['source_name'] = '掘金'
                hg_item['item_type'] = 2
                hg_item['article_id'] = d.get('article_id')
                hg_item['article_link'] = self.sub_domains + d.get('article_id')
                hg_item['title'] = d['article_info']['title']
                hg_item['is_original'] = d['article_info']['is_original']
                hg_item['view_count'] = d['article_info']['view_count']
                hg_item['collect_count'] = d['article_info']['collect_count']
                # hg_item['diff_count'] = d['article_info']['diff_count']
                hg_item['comment_count'] = d['article_info']['comment_count']
                hg_item['category_name'] = d['category']['category_name']
                hg_item['tags'] = ",".join([i['tag_name'] for i in d['tags']])
                hg_item['artical_ctime'] = d['article_info']['ctime']
                hg_item['artical_utime'] = d['article_info']['mtime']  # 需要确认是 mtime or rtime
                hg_item['brief_content'] = d['article_info']['brief_content']
                yield hg_item

        else:
            logging.error(f'request url {response.url} failed, payload: {self.payload}, error msg {response_json.get("err_msg")}')
