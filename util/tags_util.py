# -*- coding: utf-8 -*-
import logging
import os

import time
from logging.handlers import TimedRotatingFileHandler


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(msg)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_path = os.path.dirname(os.getcwd()) + '/logs/'
log_filename = log_path + time.strftime("%Y%m%d", time.localtime()) + ".log"
fh = TimedRotatingFileHandler(log_filename, when="d", encoding='utf-8', backupCount=7)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(console_handler)


CARTLIMIT = "CartLimit"
TYPE = "Type"
ATTRIBUTE = "Attribute"
ICON = "Icon"
MONSTERTYPE = "MonsterType"
CARDTYPE = "CardType"
LINK = "Link"
RARITY = "Rarity"
PACKAGE = "package"


dict_tags = {
    "CARTLIMIT": {"tags_eng_name": "CartLimit", "tags_chi_name": "卡片限制"},
    "TYPE": {"tags_eng_name": "Type", "tags_chi_name": "卡片种类"},
    "ATTRIBUTE": {"tags_eng_name": "Attribute", "tags_chi_name": "属性"},
    "ICON": {"tags_eng_name": "Icon", "tags_chi_name": "效果"},
    "MONSTERTYPE": {"tags_eng_name": "MonsterType", "tags_chi_name": "种族"},
    "CARDTYPE": {"tags_eng_name": "CardType", "tags_chi_name": "怪兽种类"},
    "LINK": {"tags_eng_name": "Link", "tags_chi_name": "Link"},
    "RARITY": {"tags_eng_name": "Rarity", "tags_chi_name": "稀有度"},
    "PACKAGE": {"tags_eng_name": "Package", "tags_chi_name": "卡包"}
}
