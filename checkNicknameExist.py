# -*- coding: utf-8 -*-
'''
Created on 2016��3��12��

@author: daniel
'''
import sys
import weibo
import webbrowser
import urllib,httplib
import urllib2
import MySQLdb
#获得新浪微博授权api
APP_KEY = '1010823506'
MY_APP_SECRET = '7bbb4decac9dfbad905a190f663ce989'
REDIRECT_URL = 'http://www.sina.com.cn/'
api = weibo.APIClient(app_key=APP_KEY,app_secret=MY_APP_SECRET,redirect_uri=REDIRECT_URL)
authorize_url = api.get_authorize_url()
webbrowser.open_new(authorize_url)
code = raw_input("input the code: ").strip()
print "111"
request = api.request_access_token(code, REDIRECT_URL)
access_token = request.access_token
expires_in = request.expires_in
api.set_access_token(access_token, expires_in)
#连接数据库获得用户昵称
conn=MySQLdb.connect(host="115.29.55.54",port=3306,user="root",passwd="chen724467110",db="b5test",charset="utf8")
cur=conn.cursor()
sqlstr="SELECT * FROM user;"
result=cur.execute(sqlstr)
for row in cur.fetchall():
	print row[1]


'''try:
    print api.users__show(screen_name="奋力前行的猪")['id']
    print api.users__show(screen_name="阅读手册")['id']
    print api.users__show(screen_name="思想聚焦12378907513639812")['id']
except :
    print "error"'''