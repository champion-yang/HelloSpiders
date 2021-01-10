# coding=utf-8
"""
@auth: xiaobei
@date: 2020/12/29
@desc:
"""

from scrapy import cmdline
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor


def start_spider(q):
    logging.info('------------ start spider ---------------')

    # 根据项目配置获取 CrawlerProcess 实例
    process = CrawlerProcess(get_project_settings())

    # 获取 spiderloader 对象，以进一步获取项目下所有爬虫名称
    spider_loader = SpiderLoader(get_project_settings())

    # 添加需要执行的爬虫
    for spidername in spider_loader.list():
        process.crawl(spidername)
    q.put(None)
    process.start()


def main():

    q = Queue()
    p = Process(target=start_spider, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


if __name__ == '__main__':
    import time
    from HelloSpiders.config.config import WAIT_TIME
    while True:
        main()
        logging.info(f'You can nearly always enjoy something if you make up your mind firmly that you will.\n'
                     f'waitting for {WAIT_TIME} s')
        time.sleep(3600)
    # cmdline.execute('scrapy crawl chinamoney'.split())
