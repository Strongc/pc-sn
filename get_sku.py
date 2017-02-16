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
from getCategory import getCategory

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
            for s0 in soup_next.find_all('li',lazy='true'):            #查找包含sku,名称,评论数量的文本
                s1=s0.select('.sell-point')[0]                    #筛选包含sku,名称的文本,class='sell-point'
                sku=re.findall('\d+(?=.html)',s1.a.get('href'))   #从"http://product.suning.com/0000000000/104618684.html"匹配sku
                #抓取名称：将名称中的促销信息去除  
                name_full=s1.a.text                               #商品全名，包含促销信息
                name_promotion=s1.a.em.string                     #促销信息
                if name_full!=name_promotion:                     #若相等，则没有促销信息
                    end_position=name_full.index(name_promotion)
                    name_sku=name_full[0:end_position]            #sku名称
                else:
                    name_sku=name_full
                s2=s0.select('.com-cnt')[0]                       #评论文本
                comments=s2.select('.num')[0].string              #评论数量
                crawldate=datetime.date.today()
                now=datetime.datetime.now()
                crawltime=now.strftime('%H:%M:%S')
                sn=[crawlid,grp,cat,sku,name_sku,comments,crawldate,crawltime,url_next]
                sql='insert into sn(id,grp,cat,sku,description,comments,crawldate,crawltime,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
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
    
    
    
