# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liuhjhj
@File           :  html_parser.py
"""
from bs4 import BeautifulSoup


def parser(html_cont):  # 根据HTML元素解析网页内容
    if html_cont is None:
        return

    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='UTF-8')
    data = {}
    # <dd class="week">2019年07月30日　星期二　己亥年六月廿八 </dd>
    day = soup.find('dd', class_="week")
    data['day'] = day.get_text()
    # <dd class="shidu"><b>湿度：28%</b><b>风向：东北风 5级</b><b>紫外线：弱</b></dd>
    humidity = soup.find('dd', class_="shidu")
    data['humidity'] = humidity.get_text()
    # <span><b>阴</b>17 ~ 31℃</span>
    tem = soup.find('dd', class_="weather").find("span")
    data['tem'] = tem.get_text()
    # <dd class="kongqi"><h5 style="background-color:#79b800;">空气质量：优</h5><h6>PM: 14</h6><span>日出: 06:11<br>日落: 19:48</span></dd>
    air = soup.find('dd', class_='kongqi')
    data['air'] = air.get_text()
    return data
