# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 12:06:23 2015
1.获取品类名称和URL:http://lib.suning.com/header/menuData-threeSortShow.jsonp?callback=threeSortShow
2.获取每个品类URL的页面数量，构造品类字典{品类名称：{品类URL：页面数量}}
3.根据品类字典构造每个品类页的URL
4.爬取该品类页URL的商品信息：sku,名称,评论数量
5.存入mysql:品类名称,sku,名称,评论数量,爬取时间,url
@author: 14020199
"""
import requests
import bs4
import pymysql
import re
import datetime
from celery import Celery
import os
from getCategory import getCategory
os.chdir('f:/python/scripts')

app=Celery('get_sku',broker='redis://localhost:6379')

@app.task  
def get_sku(grp,cat,url,crawlid):
    conn=pymysql.connect(host='127.0.0.1',user='root',passwd='1111',db='customer',charset='utf8')
    cur=conn.cursor()
    response=requests.get(url).text
    s1=re.findall('param.pageNumbers = "\d+"',response)
    s2=re.findall('\d+',s1[0])
    page_numbers=int(s2[0]) #小品类url的页面数量
    for num in range(page_numbers):
        try:
            url_next=url.replace('-0','-'+str(num),1) #构造每页的url,替代1个符合条件的字符串
            response_next=requests.get(url_next).text
            soup_next=bs4.BeautifulSoup(response_next,'html.parser')
            for string in soup_next.select('a[href$="pro_detail_tab"]'):
                sku=re.findall('\d+',string.get('href'))
                comments=string.string
                crawldate=datetime.date.today()
                now=datetime.datetime.now()
                crawltime=now.strftime('%H:%M:%S')
                sn=[crawlid,grp,cat,sku,comments,crawldate,crawltime,url_next]
                sql='insert into sn(id,grp,cat,sku,comments,crawldate,crawltime,url) values(%s,%s,%s,%s,%s,%s,%s,%s)'
                cur.execute(sql,sn)
                conn.commit()
        except:
            continue
            
if __name__=='__main__':
    crawlid=input('请输入爬虫编号（年月）：')
    category=getCategory()
    for grp in category:
        for cat in category[grp]:
            url=category[grp][cat]
            if len(url)>23 and url[23] in ('0','1'):
                get_sku.delay(grp,cat,url,crawlid)
            else:
                continue
    
    
    
