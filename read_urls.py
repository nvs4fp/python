#coding=utf-8
'''
Created on 2016年10月22日

@author: Julyzhao
'''
import pymysql.cursors
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

# get web links from given link
class webLinks(object):
    def __init__(self, weburl):
        self.sorce_url=weburl
            
    def geturls(self):
        res=urlopen(self.sorce_url).read().decode('utf-8')
        soup=BeautifulSoup(res,"html.parser") 
        urls=soup.findAll('a', href=re.compile("^/view/"))
        target_url=[]
        for url in urls:
            if not re.search("\.(jpg|JPG)", url["href"]):
                target_url.append(url.get_text()+"_"+"http://baike.baidu.com"+url["href"]) 
        return target_url


class sqldb(object): 
    def __init__(self,config):
        self.config=config
        
    def connect(self):
        return pymysql.connect(**self.config)
    
    def store(self, connection, links):
        cursor=connection.cursor()
        try:
            for link in links:
                sql="insert into view_info(name, links) values('%s','%s')" %((link.split('_')[0]),(link.split('_')[1]))
                cursor.execute(sql)
                #print(cursor.rowcount)
            connection.commit()
        except Exception as e:
            raise e
            connection.rollback()        
        finally:        
            cursor.close()
            connection.close()
        
if __name__=='__main__':
    
    #网络地址
    src="http://baike.baidu.com/view/21087.htm"
    links=webLinks(src).geturls()
    
    #数据库信息
    config = {
              'host':'127.0.0.1',
              'port':3306,
              'user':'root',
              'password':'root',
              'db':'test',
              'charset':'utf8mb4',
              'cursorclass': pymysql.cursors.DictCursor,
              }
    db1=sqldb(config) 
    conn=db1.connect()   
    db1.store(conn,links)
    i=0
    for link in links:
        i=i+1
        print(i,link)
     
    #con=pymysql.Connection(**config)
    
    

  
