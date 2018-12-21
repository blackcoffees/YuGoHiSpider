# -*- coding:utf8 -*-
import datetime

from db.PoolDB import pool


class Cart(object):
    chi_name = None
    eng_name = None
    jpe_name = None
    level = 0
    icon_url = None
    effect = None
    attack = 0
    defend = 0
    link = 0
    created = None
    updated = None
    effect_detail = None
    tags_type_id = 0

    def save(self):
        self.created = datetime.datetime.now()
        sql = """
        insert into cart(chi_name, eng_name, jpe_name, level, icon_url, effect, attack, defend, link, created,
         effect_detail, tags_type_id) 
        VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_param = (self.chi_name, self.eng_name, self.jpe_name, self.level, self.icon_url, self.effect, self.attack,
                      self.defend, self.link, self.created, self.effect_detail, self.tags_type_id)
        return pool.commit(sql, list_param)


def get_cart_by_chi_name(chi_name):
    sql = """select * from cart where chi_name = %s"""
    param = [chi_name]
    return pool.find_one(sql, param)

