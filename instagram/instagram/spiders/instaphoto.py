# -*- coding: utf-8 -*-
from selenium import webdriver
import scrapy
import json
from scrapy.http import Request,FormRequest
from instagram.items import InstagramItem
import requests
import re
import math


class InstaphotoSpider(scrapy.Spider):
	name = 'instaphoto'
	allowed_domains = ['instagram.com']
	to_Parselist = []
	#start_urls = ['http://instagram.com/']

	#使用 PhontomJS 完成登录
	def __init__(self):
		self.browser = webdriver.PhantomJS()
		print('OJBK')
		self.browser.get('https://www.instagram.com/accounts/login/')
		self.browser.find_element_by_name('username').clear()
		self.browser.find_element_by_name('password').clear()
		self.browser.find_element_by_name('username').send_keys('luojunjie20')
		self.browser.find_element_by_name('password').send_keys('19950708')
		time.sleep(1)
		

		with open('/Users/junieluo/MyGit/Instagram/toParse.txt','w+') as f:
			to_Parse = f.read()

		self.to_Parselist = to_Parse.split('  ')[:-1]

	def closed(self,spider):
		self.browser.close()
		print('OJBK1')
		

	def start_requests(self):
		for element in self.to_Parselist:
			yield [Request('www.instagram.com/%s/'%element,
				callback = self.get_user)]
			#return [Request('http://www.baidu.com/',
			 
	'''def login(self,response):
		print('OJBK1')
		return [FormRequest.from_response(response,formdata={
			'username':'luojunjie20',
			'password':'19950708'
			},
			callback = self.get_user,
			dont_filter = True
			)]'''


	#获取待处理用户
	def get_user(self,response):
		print('OJBK2')
		print(response.text)

		

	#获取关注者
	#def get_followers(self,response):

	#获取关注者的主页
	#def get_pages(self,response):

	#获取相片 url
	#def get_urls(self,response):





	#def parse(self, response):
	#    pass
