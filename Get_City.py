# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liuhjhj
@File           :  Get_City.py
"""
import re
import requests


def get_page(url):  # 获取网页内容
    head = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    timeout = 30
    try:
        page = requests.session().get(url, headers=head, timeout=timeout)
        page.encoding = 'UTF-8'
        return page.text
    except Exception as e:
        return 'Error'


# 根据正则表达式解析网页内容 regular为正则表达式
def paser_page(url, regular='<a href="/.*?/">[\u4E00-\u9FA5]+</a>'):
    text = get_page(url)
    if text == 'Error' or text is None:
        return
    patterns = re.compile(regular)
    cityname = re.findall(patterns, text)
    return cityname
