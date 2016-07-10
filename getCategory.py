# -*- coding: utf-8 -*-
"""
Created on Sat May 21 12:19:06 2016

@author: Administrator
"""
import requests
import json
import os
os.chdir('f:/python/scripts')

def getCategory(url_root='http://lib.suning.com/header/menuData-threeSortShow.jsonp?callback=threeSortShow'):
    category={}
    response_url_root=requests.get(url_root).text
    response_json=json.loads(response_url_root[14:-2])
    len_level1=len(response_json)
    for i1 in range(0,len_level1):
        level2=response_json[i1]['sub']
        len_level2=len(level2)
        for i2 in range(0,len_level2):
            if level2[i2]: #level2[i2]可能为空
                group_title=level2[i2]['t']['title']
                category.setdefault(group_title,{})
                level3=level2[i2]['s']
                len_level3=len(level3)
                for i3 in range(0,len_level3):
                    category_title=level3[i3]['title']
                    category_link=level3[i3]['link']
                    category[group_title][category_title]=category_link
    return category
