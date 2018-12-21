# -*- coding: utf-8 -*-
import os
import urllib

from PIL.Image import Image

BASE_PATH = os.path.abspath(os.path.dirname("main.py")).replace("main", "") + "image\\"


def save_image_local(url, name):
    urllib.urlretrieve(url, BASE_PATH + name + ".jpg")
    return BASE_PATH + name + ".jpg"


def rename_image(old_name, new_name):
    old_name = BASE_PATH + old_name + ".jpg"
    new_name = BASE_PATH + new_name + ".jpg"
    os.rename(old_name, new_name)

