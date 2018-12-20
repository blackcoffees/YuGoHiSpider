# -*- coding: utf-8 -*-
import os
import urllib

from PIL.Image import Image

BASE_PATH = os.path.abspath(os.path.dirname("main.py")).replace("main", "") + "image\\"


def save_image_local(url, name):
    urllib.urlretrieve(url, BASE_PATH + name + ".jpg")
    return BASE_PATH + name + ".jpg"

