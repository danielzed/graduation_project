# -*- coding:utf-8 -*-
'''
Created on 2016��3��17��

@author: daniel

在status，time的基础下，爬取了原创微博状态的转发，评论，赞数，并在数据库status——download_updata_plustime_plussocial中加入原创判断字段
is_original为1代表原创，0代表转发。
'''
import requests
from lxml import etree
from multiprocessing.dummy import Pool
import MySQLdb
import re

#数据存储
id_list=[]
id_list_test=['2695742321']
#一周更换
cook_list=[{"Cookie":"_T_WM:91f5180188f6565bb9a2f09661eedfd5;SUHB=09PNEghzqrOH1p;SUB=_2A256B0zWDeRxGeVP61YZ-SnNzD-IHXVZCFSerDV6PUJbrdAKLWbSkW1LHetiMIsoVvz2nlq9PRawxdgOKrF1dA..;gsid_CTandWM=4ugy77341VBxy1Vgxn6yzd1IZ2N;M_WEIBOCN_PARAMS=from%3Dhome"},
{"Cookie":"SUHB=09PNEghzqrOH1p; _T_WM=8f4ff72f8b0eb32df549ea51824b3813; M_WEIBOCN_PARAMS=from%3Dhome; SUB=_2A256FkNADeRxGeVJ6loS8izLzz2IHXVZ-W0IrDV6PUJbrdANLWnSkW1LHetuBq4w8gJ-WZ8iSUlJuJGSEYLvIA..; gsid_CTandWM=4u6677341SAYYH0XJitpffBiWbX"},
{"Cookie":"SUHB=09PNEghzqrOH1p; _T_WM=8f4ff72f8b0eb32df549ea51824b3813; SUB=_2A256ELs5DeRxGeNJ6VEZ8C_KyDWIHXVZ-sVxrDV6PUJbrdAKLUvZkW1LHetY3bsRn7fTywXlT2SrIVfd0pDTrA..; gsid_CTandWM=4utF77341Wa3HgDrGUiySo11naj;M_WEIBOCN_PARAMS=from%3Dhome"}]
pattern2=re.compile('\[\d+\]')
def formatTime(time):
	n=time.index('来自')
	return time[:n].strip()
#amount，例为100,则预计最大微博采集数位100-110
def getWeiById(id):
	page=1
	length=10 
	total=0
	while length>=1 and total<=1000:
		url='http://weibo.cn/%s/profile?page=%d'% (id,page)
		html=requests.get(url,cookies=cook_list[2]).content
		selector=etree.HTML(html)

		content=selector.xpath('//div[@class="c"][@id]')
		try:
			for each in content:
				transfer_author_pre=each.xpath('div[1]/span[@class="cmt"]/a[1]/@href')
				image_url=each.xpath('div[2]/a/img/@src')
				if transfer_author_pre and image_url:
					pattern=re.compile('\w+\Z')
					result=pattern.findall(transfer_author_pre[0])
					transfer_author=result[0]
					transfer_content= each.xpath('div[1]/span[@class="ctt"]/text()')[0].encode('utf-8')
					transfer_reason=each.xpath('div[3]/text()')[0].encode('utf-8')
					time=each.xpath('div[3]/span[@class="ct"]/text()')[0]
					time=formatTime(time.encode('utf-8'))
					is_original=0
					insstr="insert into userStatusPlusTimePlusSocial(uuid,tran_content,tran_author,image_url,tran_reason,time,is_original) values(%s,'%s','%s','%s','%s','%s',%d); "%(id,transfer_content,transfer_author,image_url[0],transfer_reason,time,is_original)
				elif transfer_author_pre and (not image_url):
					pattern=re.compile('\w+\Z')
					result=pattern.findall(transfer_author_pre[0])
					transfer_author=result[0]
					transfer_content= each.xpath('div[1]/span[@class="ctt"]/text()')[0].encode('utf-8')
					transfer_reason=each.xpath('div[2]/text()')[0].encode('utf-8')
					time=each.xpath('div[2]/span[@class="ct"]/text()')[0]
					time=formatTime(time.encode('utf-8'))
					is_original=0
					insstr="insert into userStatusPlusTimePlusSocial(uuid,tran_content,tran_author,tran_reason,time,is_original) values(%s,'%s','%s','%s','%s',%d); "%(id,transfer_content,transfer_author,transfer_reason,time,is_original)
				elif (not transfer_author_pre) and image_url:
					content1= each.xpath('div[1]/span[@class="ctt"]/text()')[0].encode('utf-8')
					time=each.xpath('div[2]/span[@class="ct"]/text()')[0]
					time=formatTime(time.encode('utf-8'))
					is_original=1
					content_supp_count=each.xpath('div[2]/a[3]/text()')[0]
					supp_count=pattern2.findall(content_supp_count)[0][1:-1].encode('utf-8')
					content_tran_count=each.xpath('div[2]/a[4]/text()')[0]
					tran_count=pattern2.findall(content_tran_count)[0][1:-1].encode('utf-8')
					content_comm_count=each.xpath('div[2]/a[5]/text()')[0]
					comm_count=pattern2.findall(content_comm_count)[0][1:-1].encode('utf-8')
					insstr="insert into userStatusPlusTimePlusSocial(uuid,content,image_url,time,is_original,supp_count,tran_count,comm_count) values(%s,'%s','%s','%s',%d,%s,%s,%s); "%(id,content1,image_url[0],time,is_original,supp_count,tran_count,comm_count)
					print insstr
				elif (not transfer_author_pre) and (not image_url):
					content1= each.xpath('div[1]/span[@class="ctt"]/text()')[0].encode('utf-8')
					time=each.xpath('div[1]/span[@class="ct"]/text()')[0]
					time=formatTime(time.encode('utf-8'))
					is_original=1
					content_supp_count=each.xpath('div[1]/a[1]/text()')[0]
					supp_count=pattern2.findall(content_supp_count)[0][1:-1].encode('utf-8')
					content_tran_count=each.xpath('div[1]/a[2]/text()')[0]
					tran_count=pattern2.findall(content_tran_count)[0][1:-1].encode('utf-8')
					content_comm_count=each.xpath('div[1]/a[3]/text()')[0]
					comm_count=pattern2.findall(content_comm_count)[0][1:-1].encode('utf-8')
					insstr="insert into userStatusPlusTimePlusSocial(uuid,content,time,is_original,supp_count,tran_count,comm_count) values(%s,'%s','%s',%d,%s,%s,%s); "%(id,content1,time,is_original,supp_count,tran_count,comm_count)
					print insstr
				cursor.execute(insstr)
		except Exception as e:
			print e

		#更新到下一页
		length=len(content)
		page+=1
		total+=length
	print "   ",total

# def getFollowidById(id):
# 	#关注对象的url
# 	url='http://weibo.cn/%s/follow'% id
# 	html=requests.get(url,cookies=cook).content
# 	selector=etree.HTML(html)
# 	content1=selector.xpath('//tr/td/a[1]')
# 	content2=selector.xpath('//tr/td/a[1]/@href')
# 	#问题是，每个带id的url都出现了两次，所以采用了步长为2的切片
# 	for each in content2[::2]:
#     		print each.split('/')[-1]





conn=MySQLdb.connect(host="115.29.55.54",port=3306,user="root",passwd="chen724467110",db="b5test",charset="utf8")
cursor=conn.cursor()
selstr="select * from user where uuid!='NULL'"
n=cursor.execute(selstr)
for row in cursor.fetchall():
	id_list.append(row[2])
f=open('data_test.txt','w')
for id in id_list:
	f.write('this is %s'% id)
	print id
	getWeiById(id.encode('utf-8'))
	# getFollowidById(id)
cursor.close()
f.close()
print "finished"