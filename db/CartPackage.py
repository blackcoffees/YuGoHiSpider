# -*- coding:utf8 -*-
from db.PoolDB import pool


class CartPackage(object):
    jpe_name = None
    chi_name = None
    abbreviation = None
    eng_name = None
    punish_time = None
    tags_rarity_id = 0
    created = None
    updated = None

    def save(self):
        sql = """
        insert into cart_package(jpe_name, chi_name, abbreviation, eng_name, punish_time, tags_rarity_id, created) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        param = [self.jpe_name, self.chi_name, self.abbreviation, self.eng_name, self.punish_time, self.tags_rarity_id,
                 self.created]
        return pool.commit(sql, param)


def get_cart_package_by_jpe_name(jpe_name):
    sql = """select * from cart_package where jpe_name=%s"""
    return pool.find_one(sql, param=[jpe_name])