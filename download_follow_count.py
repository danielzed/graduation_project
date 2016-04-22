# -*- coding:utf-8 -*-
import requests
from lxml import etree
from multiprocessing.dummy import Pool
import MySQLdb
import re

id_list=[]
id_list_test=['2695742321']
cook_list=[{"Cookie":"_T_WM:91f5180188f6565bb9a2f09661eedfd5;SUHB=09PNEghzqrOH1p;SUB=_2A256B0zWDeRxGeVP61YZ-SnNzD-IHXVZCFSerDV6PUJbrdAKLWbSkW1LHetiMIsoVvz2nlq9PRawxdgOKrF1dA..;gsid_CTandWM=4ugy77341VBxy1Vgxn6yzd1IZ2N;M_WEIBOCN_PARAMS=from%3Dhome"},
{"Cookie":"SUHB=09PNEghzqrOH1p; _T_WM=8f4ff72f8b0eb32df549ea51824b3813; M_WEIBOCN_PARAMS=from%3Dhome; SUB=_2A256FkNADeRxGeVJ6loS8izLzz2IHXVZ-W0IrDV6PUJbrdANLWnSkW1LHetuBq4w8gJ-WZ8iSUlJuJGSEYLvIA..; gsid_CTandWM=4u6677341SAYYH0XJitpffBiWbX"},
{"Cookie":"SUHB=09PNEghzqrOH1p; _T_WM=8f4ff72f8b0eb32df549ea51824b3813; SUB=_2A256ELs5DeRxGeNJ6VEZ8C_KyDWIHXVZ-sVxrDV6PUJbrdAKLUvZkW1LHetY3bsRn7fTywXlT2SrIVfd0pDTrA..; gsid_CTandWM=4utF77341Wa3HgDrGUiySo11naj;M_WEIBOCN_PARAMS=from%3Dhome"}]
pattern=re.compile('\[\d+\]')

def getFollowidById(id):
	#关注对象的url
	url='http://weibo.cn/%s/profile'% id
	html=requests.get(url,cookies=cook_list[2]).content
	selector=etree.HTML(html)
	content=selector.xpath('//div[@class="u"]/div[@class="tip2"]')
	for each in content:
		content_status_count=each.xpath('span[@class="tc"]/text()')[0]
		content_following_count=each.xpath('a[1]/text()')[0]
		content_follower_count=each.xpath('a[2]/text()')[0]
		status_count=pattern.findall(content_status_count)[0][1:-1].encode('utf-8')
		following_count=pattern.findall(content_following_count)[0][1:-1].encode('utf-8')
		follower_count=pattern.findall(content_follower_count)[0][1:-1].encode('utf-8')
		sqlstr="update user set status_count=%s,follower_count=%s,following_count=%s where uuid='%s';"%(status_count,follower_count,following_count,id)
		print sqlstr





conn=MySQLdb.connect(host="115.29.55.54",port=3306,user="root",passwd="chen724467110",db="b5test",charset="utf8")
cursor=conn.cursor()
selstr="select * from user where uuid!='NULL'"
n=cursor.execute(selstr)
for row in cursor.fetchall():
	id_list.append(row[2])
for id in id_list:
	getFollowidById(id.encode('utf-8'))
cursor.close()
print "finished"