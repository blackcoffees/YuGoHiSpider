# -*- coding:utf8 -*-
import datetime

from db.PoolDB import pool


def get_spider_now_page():
    sql = """
        select * from spider_conf where name="spider_now_page"
    """
    result = pool.find_one(sql)
    return result.get("value")


def set_spider_now_page(new_page):
    sql = """
        update spider_conf set value = %s, updated=%s where name="spider_now_page"
    """
    param = [new_page, datetime.datetime.now()]
    pool.commit(sql, param)
