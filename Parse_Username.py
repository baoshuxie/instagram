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

#定义'关注的人'类,包含id,username,is_private三个属性
class Follower(object):
	def __init__(self,id,username,is_private):
		self.id = id
		self.username = username
		self.is_private = is_private

#定义'人'类,继承自 follower, 不仅包含follower 原有的属性,还包括 count(关注者数量),page_count(关注的人有几页),followers(关注的人列表)
class Person(Follower):
	def __init__(self,follower,count,page_count,followers):
		self.id = follower.id
		self.username = follower.username
		self.is_private = follower.is_private
		self.count = count
		self.page_count = page_count
		self.followers = followers

'''
def form_header(referer):
	headers = {
		'Host': 'fmn.rrimg.com',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer)
	
	}

	return headers
'''

def login(username,passwd,browser):
	browser.implicitly_wait(1)
	browser.set_page_load_timeout(20)
	browser.set_script_timeout(20)

	base_url = 'https://www.instagram.com/accounts/login/'
	browser.get(base_url)
	browser.implicitly_wait(1)

	account = browser.find_element_by_xpath("//input[@name='username']")
	#print(account)
	account.clear()
	account.send_keys(username)
	print('账号输入完成')

	password = browser.find_element_by_xpath("//input[@name='password']")
	password.clear()
	#print(password)
	password.send_keys(passwd)
	print('密码输入完成')

	button = browser.find_elements_by_xpath('//button')[1]
	
	print(button.text)
	button.click()
	print('开始登录')
	browser.implicitly_wait(3)

	time.sleep(1)

	#browser.get('https://www.instagram.com/luojunjie20')
	#browser.implicitly_wait(1)

def get_followers(user)
	page_count = 0
	followers = []
	query_hash = 
	url = 'https://www.instagram.com/graphql/query/?query_hash={}}&variables={"id":{},"first":{}}'.format(query_hash,id,first_count)

	def get_next_page(url,page_count,followers)
		browser.get()
		browser.implicitly_wait(1)
		page_count+=1
		html= browser.page_source.text
		#print(html)
		html = html.split('>')[5].split('<')[0].strip()
		#print(html)
		js = json.loads(html)
		count = js['data']['user']['edge_follow']['count']
		has_next_page = js['data']['user']['edge_follow']['page_info']['has_next_page']
		end_cursor = js['data']['user']['edge_follow']['page_info']['end_cursor'] 
		nodes = js['data']['user']['edge_follow']['edges']
		#print(nodes)
		
		for node in nodes:
			id = node['node']['id']
			username = node['node']['username']
			is_private = node['node']['is_private']
			follower = Follower(id,username,is_private)
			followers.append(follower)

		if has_next_page == 'true':
			next_page = 
			get_next_page()

		person = Person(user,count,page_count,followers)
		return person

	person1 = get_next_page(url)
	print(person1.id,person1.username,person1.is_private,person1.count,person1.page_count,person1.followers)

def main():
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
	
	browser = webdriver.PhantomJS(service_args=service_args,desired_capabilities=dcap)
	usernames = []
	login('luojunejie20','19950708',browser)

	with open('/Users/junjieluo/MyGit/instagram/toParse.txt','a+') as f:
		toParse = f.read()

	toParseList = toParse.split('  ')[:-1]

	with open('/Users/junjieluo/MyGit/instagram/Parsed.txt','a+')
		Parsed = f.read()
	
	ParsedSet = set(Parsed.split('  ')[:-1])

	limit = 0
   	
	for username in toParselist:
		if limit <= 100:
			pass
		else:
			limit += 1

		if username in ParsedSet:
			continue
		else:
			toParselist.remove(username)
			ParsedSet.add(username)
			followers = get_followers(username)
			tem_list = toParselist + followers

	with open('/Users/junjieluo/MyGit/instagram/toParse.txt','w+') as f:
		for username in tem_list:
			f.write(username + '  ')
	with open('/Users/unjieluo/MyGit/instagram/Parsed.txt','w+') as f:
		for username in ParsedSet:
			f.write(username + '  ')

	browser.quit()
	print('selenium已退出')
	


#def get_followers(username):
#	url = 'http://www.instagram.com/%s/'%username
#	followers = 
#
#	return followers 
get_urls(100)
