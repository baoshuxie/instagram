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
	toParseList = []
	ParsedSet = set()
	id = 1
	#start_urls = ['http://instagram.com/']

	#使用 PhontomJS 完成登录
	def start_requests(self,response):
		with open('/Users/junjieluo/MyGit/instagram/toParse.txt','w+') as f:
			toParse = f.read()

		self.toParseList = toParse.split('  ')[:-1]

		with open('/Users/junjieluo/MyGit/instagram/Parsed.txt','w+')
			Parsed = f.read()
	
		self.ParsedSet = set(Parsed.split('  ')[:-1])

		for username in self.toParseList:
			if username in self.ParsedSet:
				continue
			else:
				self.toParseList.remove(username)
				self.ParsedSet.add(username)
				self.id += 1
				url = 'http://www.instagram.com/%s/'%username
				yield Request(url,
					meta = {'username':username}
					callback = self.parse_photo_urls)

	def parse_photo_urls(self,response):
		photo_urls = response.xpath()

		for photo_url in photo_urls:
			item = 





	#def parse(self, response):
	#    pass
