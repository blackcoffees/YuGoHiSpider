# -*- coding:utf8 -*-
import datetime

from db.PoolDB import pool


class CartDetail(object):
    id = 0
    cart_id = 0
    cart_tags_id = 0
    created = None
    cart_tags_eng_name = None

    def save(self):
        sql = """insert into cart_detail(cart_id, cart_tags_id, created, cart_tags_eng_name) values (%s, %s, %s, %s)"""
        param = [self.cart_id, self.cart_tags_id, datetime.datetime.now(), self.cart_tags_eng_name]
        return pool.commit(sql, param)


def create_cart_detail(cart_tags_id, cart_tags_eng_name):
    cart_detail = CartDetail()
    cart_detail.cart_tags_id = cart_tags_id
    cart_detail.cart_tags_eng_name = cart_tags_eng_name
    return cart_detail