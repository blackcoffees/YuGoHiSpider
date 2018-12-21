# -*- coding:utf8 -*-
from db.PoolDB import pool
from util.tags_util import RARITY, dict_tags, PACKAGE


class CartTags(object):
    id = 0
    chi_name = None
    jap_name = None
    eng_name = None
    tags_chi_name = None
    tags_eng_name = None

    def save(self):
        sql = """
        insert into cart_tags(chi_name, jap_name, eng_name, tags_chi_name, tags_eng_name)
        VALUES (%s, %s, %s, %s, %s)
        """
        param = [self.chi_name, self.jap_name, self.eng_name, self.tags_chi_name, self.tags_eng_name]
        return pool.commit(sql, param)


def get_tags_rarity(value):
    tags_rarity = get_tags_by_tags_eng_name_equal(RARITY, value)
    if tags_rarity:
        return tags_rarity
    else:
        if dict_tags.get(RARITY.upper()):
            cart_tags = CartTags()
            cart_tags.chi_name = value
            cart_tags.eng_name = value
            cart_tags.tags_chi_name = dict_tags.get(RARITY.upper()).get("tags_chi_name")
            cart_tags.tags_eng_name = dict_tags.get(RARITY.upper()).get("tags_eng_name")
            cart_tags.save()
            return get_tags_rarity(value)


def get_tags_by_name(name, tags_eng_name=None):
    if tags_eng_name:
        sql = """select id from cart_tags where tags_eng_name=%s and chi_name like '%%s%'"""
        param = [tags_eng_name, name]
    else:
        sql = """select id from cart_tags where chi_name like '%%s%'"""
        param = [name]
    return pool.find_one(sql, param=param)


def get_tags_by_tags_eng_name(tags_eng_name, value, tags_eng_name2=None, is_equal=False):
    tags_eng_name = tags_eng_name.upper()
    if tags_eng_name != "PACKAGE":
        value = value.replace(" ", "")
        value = value.replace("\n", "")
    if not value:
        return None
    if tags_eng_name2:
        tags_eng_name2 = tags_eng_name2.upper()
    # sql = """select * from cart_tags where tags_eng_name="%s" and chi_name like "%%%%%s%%%%" """ %\
    #       (tags_eng_name, value)
    sql = """select * from cart_tags where tags_eng_name=%s and chi_name =%s"""
    cart_tags = pool.find_one(sql, [tags_eng_name, value])
    if cart_tags:
        return cart_tags
    elif tags_eng_name2:
        # sql = """select * from cart_tags where tags_eng_name in ("%s", "%s") and chi_name like "%%%%%s%%%%" """ % (
        #     tags_eng_name, tags_eng_name2, value)
        sql = """select * from cart_tags where tags_eng_name in (%s, %s) and chi_name =%s """
        cart_tags = pool.find_one(sql, [tags_eng_name, tags_eng_name2, value])
        if cart_tags:
            return cart_tags
    if dict_tags.get(tags_eng_name):
        cart_tags = CartTags()
        cart_tags.chi_name = value
        cart_tags.eng_name = value
        cart_tags.jap_name = value
        cart_tags.tags_chi_name = dict_tags.get(tags_eng_name).get("tags_chi_name")
        cart_tags.tags_eng_name = dict_tags.get(tags_eng_name).get("tags_eng_name")
        cart_tags.save()
        return get_tags_by_tags_eng_name(tags_eng_name, value, tags_eng_name2)
    else:
        print u"该分类不存在%s, %s" % (tags_eng_name, value)


def get_tags_by_tags_eng_name_equal(tags_eng_name, value):
    sql = """select * from cart_tags where tags_eng_name=%s and chi_name=%s"""
    param = [tags_eng_name, value]
    return pool.find_one(sql, param)