# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 17:01:36 2016
把苏宁的SKU按评论数量倒排序并取前20000个
@author: 14020199
"""
import pymysql
import pandas as pd

def get_sku():
    conn=pymysql.connect(host='127.0.0.1',user='root',passwd='1111',db='customer',charset='gbk')
    cur=conn.cursor()
    #从mysql获取sku及评论数量
    sql='select sku,comments from sn where id="201605"'#取sn表中的sku和评论数量
    sku=pd.read_sql(sql,conn)#读取
    sku=sku.drop_duplicates('sku')#去重
    sku.sort_values('comments',ascending=False,inplace=True)#按评论数量倒排序
    sku2=sku[0:50000]['sku']
    cur.close()
    conn.close()
    return sku2


'''
def get_sku():
    conn=pymysql.connect(host='127.0.0.1',user='root',passwd='1111',db='customer',charset='gbk')
    cur=conn.cursor()
    #从mysql获取sku及评论数量
    sql='select sku,comments from sn where id="201605"'#取sn表中的sku和评论数量
    sku=pd.read_sql(sql,conn)#读取
    sku=sku.drop_duplicates('sku')#去重
    sku.sort_values('comments',ascending=False,inplace=True)#按评论数量倒排序
    sku['cum_comments']=sku['comments'].cumsum()#累计求和
    sku['cum_ratio']=sku['cum_comments']/sum(sku.comments)#求累计比
    sku_a=sku[sku.cum_ratio<=0.9]['sku']#2w，a类占90%
    sku_b=sku[(sku.cum_ratio>0.9)&(sku.cum_ratio<=0.97)]['sku']#4w，b类占7%
    sku_c=sku[(sku.cum_ratio>0.97)&(sku.comments>0)]['sku']#20w，c类占3%，且评论数量>0
    cur.close()
    conn.close()
    return sku_a,sku_b,sku_c
'''
