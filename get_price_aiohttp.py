# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 21:14:15 2016

@author: Administrator
"""

import asyncio
import aiohttp
import aiomysql
import datetime
import os
import queue
import sku_abc
import time
import json

os.chdir('f:/python/scripts')

async def get_price(sku):
    url_base='http://www.suning.com/webapp/wcs/stores/ItemPrice/000000000'
    url=url_base+str(sku)+'__9017_10106_5.html'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_sku=await response.read()
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
            conn=await aiomysql.connect(host='127.0.0.1',user='root',password='1111',
                                        db='customer')
            cur=await conn.cursor()
            sql='insert into price_sn values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            await cur.execute(sql,price)
            await conn.commit()
            await cur.close()
            conn.close()
            
if __name__=='__main__':
    time_start=input('输入开始爬取的时间（2位数）：')
    while True:
        now=datetime.datetime.now()
        hour=now.strftime('%H')
        weekday=now.weekday()
        if hour==time_start:
            skus=sku_abc.get_sku()
            skus_queue=queue.Queue()
            for s in skus:
                skus_queue.put(s)
            while skus_queue.qsize()>0:
                loop=asyncio.get_event_loop()
                tasks=[]
                for n in range(0,200):
                    task=asyncio.ensure_future(get_price(skus_queue.get()))
                    tasks.append(task)
                loop.run_until_complete(asyncio.wait(tasks))
        time.sleep(1800)