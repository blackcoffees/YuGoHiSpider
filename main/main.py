# -*- coding:utf8 -*-
from spider.spider import CardSpider

if __name__ == "__main__":
    try:
        a = CardSpider()
        a.work()
    except BaseException as e:
        print e
