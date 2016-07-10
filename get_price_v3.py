# -*- coding: utf-8 -*-
"""
Created on Wed May 25 21:24:44 2016

@author: Administrator
"""

import requests
import datetime
import pymysql
import json
import time
import os
os.chdir('f:\python\scripts\sn')
import sku_abc

def get_price(sku):
    url_base='http://www.suning.com/webapp/wcs/stores/ItemPrice/000000000'
    conn=pymysql.connect(host='127.0.0.1',user='root',passwd='1111',db='customer',charset='gbk')
    cur=conn.cursor()
    try:
        price=[]
        url=url_base+str(sku)+'__9017_10106_5.html'
        response_sku=requests.get(url).text
        json_sku=json.loads(response_sku[15:-2])
        inventory=json_sku['saleInfo'][0]['invStatus']
        net=json_sku['saleInfo'][0]['netPrice']
        promotion=json_sku['saleInfo'][0]['promotionPrice']
        ref=json_sku['saleInfo'][0]['refPrice']
        salesorg=json_sku['saleInfo'][0]['salesOrg']
        vendor=json_sku['saleInfo'][0]['vendorCode']
        crawldate=datetime.date.today()
        now=datetime.datetime.now()
        crawltime=now.strftime('%H:%M')
        price=[sku,inventory,net,promotion,ref,salesorg,vendor,crawldate,crawltime]
        sql='insert into price_sn values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cur.execute(sql,price)
        conn.commit()
    except:
        error=[]
        crawldate=datetime.date.today()
        error=[sku,crawldate]
        sql='insert into price_sn_error values(%s,%s)'
        cur.execute(sql,error)
        conn.commit()

if __name__=='__main__':
    time_start=input('输入开始爬取的时间（2位数）：')
    skus=sku_abc.get_sku()
    while True:
        now=datetime.datetime.now()
        hour=now.strftime('%H')
        if hour==time_start:
            for sku in skus:
                get_price(sku)
        time.sleep(1800)