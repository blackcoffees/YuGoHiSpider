# -*- coding:utf8 -*-
import json
import re

import requests
from bs4 import BeautifulSoup, NavigableString

from db.CartDetail import CartDetail, create_cart_detail
from db.Cart import Cart, get_cart_by_chi_name
from db.CartPackage import CartPackage, get_cart_package_by_jpe_name
from db.CartTags import get_tags_rarity, CartTags, get_tags_by_tags_eng_name
from db.SpiderConf import get_spider_now_page, set_spider_now_page
from util.image_util import save_image_local
from util.tags_util import CARTLIMIT, MONSTERTYPE, ATTRIBUTE, LINK, \
    CARDTYPE, TYPE, ICON, RARITY, PACKAGE


class CardSpider():
    def work(self):
        page = get_spider_now_page()
        page = 942
        while True:
            try:
                list_card_url = "https://www.ourocg.cn/card/list-5/%s" % page
                response_cards = requests.get(list_card_url)
                soup_cards = BeautifulSoup(response_cards.text, "html.parser")
                patter = re.compile(r"__STORE__ = (.*)}};")
                script_cards = soup_cards.find("script", text=patter)
                if not script_cards:
                    continue
                json_cards = json.loads(script_cards.text.split("window.__STORE__ = ")[1].split(";")[0])
                if not json_cards.get("cards") or len(json_cards.get("cards")) == 0:
                    print "收集完成"
                    set_spider_now_page(1)
                    break
                for card in json_cards.get("cards"):
                    card_url = card.get("href")
                    response_card = requests.get(card_url)
                    soup_card = BeautifulSoup(response_card.content.replace("\n", ""), "html.parser")
                    div_card_detail = soup_card.find("div", attrs={"class": "card el-row"})
                    cart = Cart()
                    list_cart_detail = list()
                    # 卡片名字
                    div_name_class = "val el-col-xs-18 el-col-sm-12 el-col-md-14 el-col-sm-pull-8 el-col-md-pull-6"
                    list_div_name = div_card_detail.find_all("div", attrs={"class": div_name_class})
                    chi_name = ""
                    eng_name = ""
                    jpe_name = ""
                    if list_div_name[0].find("div"):
                        chi_name = list_div_name[0].find("div").text.replace(" ", "")
                    if list_div_name[1]:
                        jpe_name = list_div_name[1].text.replace(" ", "")
                    if list_div_name[2]:
                        eng_name = list_div_name[2].text.replace(" ", "")
                    print chi_name
                    # 卡片是否存在
                    if get_cart_by_chi_name(chi_name):
                        continue
                    cart.chi_name = chi_name
                    cart.eng_name = eng_name
                    cart.jpe_name = jpe_name
                    # 怪兽种类
                    if len(list_div_name) >= 4:
                        cart_list_cart_type = list()
                        span_list_cart_type = list_div_name[3].find_all("span")
                        for index_span_cart_type in range(len(span_list_cart_type)):
                            span_cart_type_text = span_list_cart_type[index_span_cart_type].text
                            if index_span_cart_type == 0:
                                # 卡片种类
                                tags_type = get_tags_by_tags_eng_name(TYPE, span_cart_type_text)
                                cart.tags_type_id = tags_type.get("id")
                            else:
                                tags_cart_type = get_tags_by_tags_eng_name(CARDTYPE, span_cart_type_text, ICON)
                                if tags_cart_type:
                                    cart_list_cart_type.append(tags_cart_type.get("id"))
                    # 保存图片
                    icon_url = div_card_detail.find("div", attrs={"class": "img"}).find("div").attrs.get("style")\
                                .split("background: url(")[1].split(")")[0].replace("'", "")
                    cart.icon_url = save_image_local(icon_url, chi_name)
                    # 使用限制
                    div_cart_limit_class_name = "val el-col-xs-10 el-col-sm-6 el-col-sm-pull-8 el-col-md-8 el-col-md-pull-6"
                    div_cart_limit = div_card_detail.find_all("div", attrs={"class": div_cart_limit_class_name})
                    if len(div_cart_limit) > 0:
                        page_cart_limit = div_cart_limit[0].text
                        tags_cart_limit = get_tags_by_tags_eng_name(CARTLIMIT, page_cart_limit)
                        if tags_cart_limit:
                            cart.tags_card_limit_id = tags_cart_limit.get("id")
                    # 其他
                    other_head_class_name = "head el-col-xs-6 el-col-sm-4 "
                    next_div_other_head = div_card_detail.find("div", attrs={"class": other_head_class_name})
                    next_div_other_value = next_div_other_head.next_sibling.next_sibling
                    while True:
                        if next_div_other_head:
                            page_head_text = next_div_other_head.text.replace(" ", "").replace("\n", "")
                            # 种族
                            if page_head_text == u"种族":
                                page_monster_type = next_div_other_value.text
                                if u"类" in page_monster_type:
                                    page_monster_type = page_monster_type.replace(u"类", u"族")
                                if u"族" not in page_monster_type:
                                    page_monster_type = page_monster_type + u"族"
                                tags_monster_type = get_tags_by_tags_eng_name(MONSTERTYPE, page_monster_type)
                                if tags_monster_type:
                                    list_cart_detail.append(create_cart_detail(tags_monster_type.get("id"),
                                                                               tags_monster_type.get("tags_eng_name")))
                            # 属性
                            elif page_head_text == u"属性":
                                page_attribute = next_div_other_value.text
                                tags_attribute = get_tags_by_tags_eng_name(ATTRIBUTE, page_attribute)
                                if tags_attribute:
                                    list_cart_detail.append(create_cart_detail(tags_monster_type.get("id"),
                                                                               tags_monster_type.get("tags_eng_name")))
                            # 星级
                            elif page_head_text == u"星级":
                                page_level = next_div_other_value.text
                                if page_level:
                                    cart.level = int(page_level)
                                else:
                                    cart.level = 0
                            # 攻击
                            elif page_head_text == u"攻击力":
                                page_attack = next_div_other_value.text
                                if page_attack:
                                    cart.attack = int(page_attack)
                                else:
                                    cart.attack = 0
                            # 守备,与link互斥
                            elif page_head_text == u"防御力":
                                cart.link = 0
                                page_defend = next_div_other_value.text
                                if page_defend:
                                    cart.defend = int(page_defend)
                                else:
                                    cart.defend = 0
                                break
                            # link
                            elif page_head_text == u"LINK":
                                cart.defend = 0
                                # page_link = next_div_other_value.text
                                page_link = div_card_detail.find("div", attrs={"class": "val el-col-xs-6 el-col-sm-4 el-col-md-6"}).text
                                if page_link:
                                    cart.link = int(page_link)
                                else:
                                    cart.link = 0
                                break
                            # 稀有度
                            if page_head_text == u"罕见度":
                                list_page_rarity = next_div_other_value.text.replace(" ", "").split(u"，")
                                for page_rarity in list_page_rarity:
                                    tags_rarity = get_tags_by_tags_eng_name(RARITY, page_rarity)
                                    if tags_rarity:
                                        list_cart_detail.append(create_cart_detail(tags_monster_type.get("id"),
                                                                                   tags_monster_type.get(
                                                                                       "tags_eng_name")))
                            # 下一行数据
                            next_div_other_head = next_div_other_value.next_sibling
                            while True:
                                try:
                                    if not next_div_other_head:
                                        break
                                    if next_div_other_head and type(next_div_other_head) != NavigableString and \
                                                    other_head_class_name in " ".join(next_div_other_head.attrs.get("class")):
                                        break
                                    next_div_other_head = next_div_other_head.next_sibling
                                except BaseException:
                                    break
                            if not next_div_other_head:
                                break
                            next_div_other_value = next_div_other_head.next_sibling.next_sibling
                        else:
                            break
                    # 效果
                    div_effect = div_card_detail.find("div", attrs={"class", "val el-col-24 effect"})\
                        .find("div", attrs={"class", "text_nw"})
                    cart.effect = div_effect.text.replace(" ", "")
                    # 链接方向
                    if div_card_detail.find("div", attrs={"class": "linkMark"}):
                        div_list_link = div_card_detail.find("div", attrs={"class": "linkMark"}).find("i")
                        for index_div_link in range(len(div_list_link)):
                            if "on" in div_list_link[index_div_link].attrs("class"):
                                if index_div_link == 0:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Lower Left")
                                elif index_div_link == 1:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Down")
                                elif index_div_link == 2:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Lower Right")
                                elif index_div_link == 3:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Left")
                                elif index_div_link == 4:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Right")
                                elif index_div_link == 5:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Upper Left")
                                elif index_div_link == 6:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Upper")
                                elif index_div_link == 7:
                                    tags_link = get_tags_by_tags_eng_name(LINK, "Upper Right")
                                list_cart_detail.append(create_cart_detail(tags_link.get("id"),
                                                                           tags_link.get("tags_eng_name")))
                    # 卡包
                    table_cart_package = div_card_detail.find("table", attrs={"id", "pack_table_main"})
                    if table_cart_package:
                        tr_list_cart_package = table_cart_package.find("tr")[1:]
                        for tr_cart_package in tr_list_cart_package:
                            # 新增卡包
                            jpe_name = tr_cart_package.find("a").text
                            cart_package = get_cart_package_by_jpe_name(jpe_name)
                            if not cart_package:
                                cart_package = CartPackage()
                                cart_package.jpe_name = jpe_name
                                cart_package.punish_time = tr_cart_package.find("small").text
                                cart_package.abbreviation = tr_cart_package.find("a").attrs.get("href").split("package/")[1].split("/")[0]
                                page_rarity = tr_cart_package.find_all("td")[1:].text
                                tags_rarity = get_tags_rarity(page_rarity)
                                cart_package.tags_rarity_id = tags_rarity.get("id")
                                cart_package.save()
                                cart_package = get_cart_package_by_jpe_name(jpe_name)
                            # 新增cart_tags
                            tags_package = get_tags_by_tags_eng_name(PACKAGE, cart_package.get("jpe_name"))
                            # 新增cart_detail
                            list_cart_detail.append(create_cart_detail(tags_package.get("id"),
                                                                       cart_package.get("tags_eng_name")))

                    # 效果详细描述
                    div_effect_detail = soup_card.find("div", attrs={"id": "adjust"})
                    if div_effect_detail:
                        list_li_card_detail = div_effect_detail.find_all("li")
                        if list_li_card_detail and len(list_li_card_detail) >= 1:
                            cart.effect_detail = div_effect_detail.find_all("li")[1].text.replace("\r", "\n")
                    cart_id = cart.save()
                    # 保存cart_detail
                    for cart_detail in list_cart_detail:
                        cart_detail.cart_id = cart_id
                        cart_detail.save()
            except BaseException as e:
                print e
            finally:
                page += 1






