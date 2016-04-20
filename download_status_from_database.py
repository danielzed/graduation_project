#-*- coding:utf-8 -*-
import MySQLdb
import jieba
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

#id列表，原创内容分词结果列表，昵称列表
id_list=[]
corpus=[]
name_list=[]

#获取停用词列表
stopwords=[]
with open("dictionary/stopwords.txt") as f:
	for row in f.readlines():
		stopwords.append(row.strip().decode('utf-8'))
#链接陈明朝数据库
conn=MySQLdb.connect(host="115.29.55.54",port=3306,user="root",passwd="chen724467110",charset="utf8",db="b5test")
cursor=conn.cursor()
sqlstr="select uuid,userName from user where uuid is not null;"
n=cursor.execute(sqlstr)
#取得数据库内用户id和昵称列表
for row in cursor.fetchall():
	id_list.append(row[0])
	name_list.append(row[1].encode('utf-8'))
	index=0
#获得每个用户的内容和转发原因等原创内容
for id in id_list:
	sqlstr="select content,tran_reason from userStatus where uuid='%s';" % id
	n=cursor.execute(sqlstr)
	content=""
	word_no_stopwords=""
	for status in cursor.fetchall():
		content=content+status[0]+status[1]
	seg_list=jieba.cut(content)
	for word in seg_list:
		if word not in stopwords:
			word_no_stopwords=word_no_stopwords+" "+word
	corpus.append(word_no_stopwords)
for row in corpus:
	print row.encode('utf-8')

# for row in corpus:
# 	print row.encode('utf-8')