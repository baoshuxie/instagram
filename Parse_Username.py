#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

__author__ = 'baoshuxie'

import os
import requests
from selenium import webdriver
from datetime import datetime
import time
import math
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json 
import pymysql
import pymysql.cursors

#定义'关注的人'类,包含id,username,is_private三个属性
class Follower(object):
	def __init__(self,username,id,is_private):
		self.id = id
		self.name = username
		self.is_private = is_private

#定义'人'类,继承自 follower, 不仅包含follower 原有的属性,还包括 count(关注者数量),page_count(关注的人有几页),followers(关注的人列表)
class Person(Follower):
	def __init__(self,follower,followers):
		self.id = follower.id
		self.name = follower.name
		self.followers = followers


#登录
def login():
	global browser
	#完成登录以及数据库连接
	browser.implicitly_wait(1)
	browser.set_page_load_timeout(20)
	browser.set_script_timeout(20)

	base_url = 'https://www.instagram.com/accounts/login/'
	browser.get(base_url)
	browser.implicitly_wait(1)

	account = browser.find_element_by_xpath("//input[@name='username']")
	#print(account)
	account.clear()
	account.send_keys('luojunjie20')
	print('账号输入完成')

	password = browser.find_element_by_xpath("//input[@name='password']")
	password.clear()
	#print(password)
	password.send_keys('19950708')
	print('密码输入完成')

	button = browser.find_elements_by_xpath('//button')[1]
	
	print(button.text)
	button.click()
	print('开始登录')
	browser.implicitly_wait(3)

	time.sleep(1)

#连接数据库
def connect_db():
	connect = pymysql.connect(
			host = 'localhost',
			port = 3306,
			db = 'instagram',
			user = 'root',
			passwd = '19950708',
			charset = 'utf8'
			)
	cursor = connect.cursor()
	print('游标创建')
	connect.autocommit(1)
	print('自动提交')
	return cursor

#从数据库中选取待爬取的 follower
def select_to_Parse(cursor):
	to_Parse = "select follower_name,follower_id,is_private from Followers where parsed='0'"
	cursor.execute(to_Parse)
	result = cursor.fetchall()
	print(result)
	#构造一个数组,数组中的每一个元素是由 result 构造出来的 Follower 实例
	toParseList = [Follower(x[0],x[1],x[2]) for x in result]
	print('待爬取的用户有:')
	for a in toParseList:
		print(a.name)

	return toParseList


#获取关注者,get_followers中用到的方法
def get_next_page(url,followers):
	global browser
	global query_hash
	global id

	browser.get(url)
	browser.implicitly_wait(1)
	#page_count+=1
	html= browser.page_source
	#print(html)
	html = html.split('>')[5].split('<')[0].strip()
	print(html)
	js = json.loads(html)
	#count = js['data']['user']['edge_follow']['count']
	has_next_page = js['data']['user']['edge_follow']['page_info']['has_next_page']
	print(has_next_page)
	end_cursor = js['data']['user']['edge_follow']['page_info']['end_cursor'] 
	nodes = js['data']['user']['edge_follow']['edges']
	#print(nodes)
	
	for node in nodes:
		follower_id = node['node']['id']
		username = node['node']['username']
		is_private = node['node']['is_private']
		follower = Follower(username,follower_id,is_private)
		followers.append(follower)

	'''在此处要构造下一页的网址,可以采用 query_hash 来构造,也可以采用 query_id 来构造,关键是每一个符号都需要转化成 ASCII 编码
	若采用 query_hash 来构造, next_page = 'https://www.instagram.com/graphql/query/?query_hash={}&variables={"id":{},"first":{},"after":{}}'.format(query_hash,id,next_page,end_cursor)
	请注意,不能直接使用这个网址,需要将其全部转化为 ASCII 码,即next_page = 'https://www.instagram.com/graphql/query/?query_hash={}&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A{}%2C%22after%22%3A%22{}%22%7D'.format(query_hash,id,next_count,end_cursor)
	若采用query_id 来构造,next_page = 'https://www.instagram.com/graphql/query/?query_id={}&variables={"id":{},"first":{},"after":{}}'.format(query_id,id,next_page,end_cursor)
	即next_page = 'https://www.instagram.com/graphql/query/?query_id={}&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A{}%2C%22after%22%3A%22{}%22%7D'.format(query_id,id,next_count,end_cursor)
	'''
	if has_next_page == True:
		next_count = 12		#这个 next_count 随便设置,最高不超过15
		query_id = 17851374694183129
		next_page = 'https://www.instagram.com/graphql/query/?query_hash={}&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A{}%2C%22after%22%3A%22{}%22%7D'.format(query_hash,id,next_count,end_cursor)
		get_next_page(next_page,followers)

	return followers
	

#获取关注者
def get_followers(user):
	#page_count = 0
	global browser
	global query_hash
	global id
	query_hash = '9335e35a1b280f082a47b98c5aa10fa4'
	id = user.id
	first_count=24
	url = 'https://www.instagram.com/graphql/query/?query_hash={}&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A{}%7D'.format(query_hash,id,first_count)
	print('正在访问'+url)
	print('正在爬取用户%s'%user.name)
	followers = get_next_page(url,[])
	person = Person(user,followers)
	print('person的id是{},person的username是{}\n'.format(user.id,user.name))
	return person


#爬取完一个人的关注者之后,修改数据库(将当前数据库)
def modify_flag_add(cursor,user,person):
	global browser
	modify_flag = 'update followers set parsed="1" where follower_name="%s"'%user.name
	cursor.execute(modify_flag)
	print('用户%s状态已更改'%user.name)

	for follower in person.followers:
		is_Parsed = 'select count(*) from followers where follower_name="%s"'%follower.name
		cursor.execute(is_Parsed)
		result = cursor.fetchone()
		#print(result)

		if result == (0,):
			add_follower = 'insert into followers values("{}","{}","{}","{}","{}","0","0")'.format(user.name,user.id,follower.name,follower.id,follower.is_private)
			cursor.execute(add_follower)
		else:
			add_follower = 'insert into followers values("{}","{}","{}","{}","{}","1","0")'.format(user.name,user.id,follower.name,follower.id,follower.is_private)
			cursor.execute(add_follower)
		print('正在向数据库中插入关注者%s的数据'%follower.name)

def main():
	#配置
	service_args = [
	'--proxy=http://127.0.0.1:1087',    # 代理 IP：port    （eg：192.168.0.28:808）
	'--proxy-type=https',            # 代理类型：http/https
	'--load-images=no',           # 关闭图片加载（可选）
	'--disk-cache=yes',            # 开启缓存（可选）
	'--ignore-ssl-errors=true'    # 忽略https错误（可选）
	]

	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = (
	"Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
	)
	
	#完成登录以及数据库连接
	global browser
	browser = webdriver.PhantomJS(service_args=service_args,desired_capabilities=dcap)
	
	login()
	cursor = connect_db()
	#user=Follower('luojunjie20','8091752170','false')
	toParseList = select_to_Parse(cursor)
	for toParse_user in toParseList:
		#print(toParse_user.name)
		if toParse_user.is_private == 'True':
			modify_flag = 'update followers set parsed="1" where follower_name="%s"'%toParse_user.name
		else:
			person = get_followers(toParse_user)
			modify_flag_add(cursor,toParse_user,person)

	browser.quit()
	print('selenium已退出')

main()
	

