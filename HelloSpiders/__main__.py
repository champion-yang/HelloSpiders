# coding=utf-8
"""
@auth: xiaobei
@date: 2020/12/29
@desc:
"""
from scrapy import cmdline


def main():
    cmdline.execute('scrapy crawl toutiao'.split())


if __name__ == '__main__':
    main()
