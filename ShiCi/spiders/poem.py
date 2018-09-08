# -*- coding:utf-8 -*-

import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from ShiCi.items import ShiciItem
import json

class PoemSpider(scrapy.Spider):
	"""docstring for PoemSpider"""
	
	name = 'poem'
	allowed_domains = ['gushiwen.org']
	bash_url = 'https://www.gushiwen.org/shiwen/'
	bashurl = '.aspx'

	# 开始爬取，获取诗词详情页url
	def start_requests(self):
		for i in xrange(1,2):
			url = self.bash_url + 'default_0A0A' + str(i) + self.bashurl
			print url
			yield Request(url, self.parse)

	# 获取每首诗词的id
	def poemDetailURL(self,x):
		_73add8822103_aspx = x.split('_')[-1]
		_73add8822103 = _73add8822103_aspx.split('.')[0]
		return 'https://so.gushiwen.org/shiwenv_' + _73add8822103 + '.aspx'

	# 获取诗词的详情页内容
	def parse(self, response):

		textarea = response.selector.xpath('//textarea/text()').extract()
		urls = map(self.poemDetailURL, textarea)
		for url in urls:
			yield Request(url, self.poemDetail)
		


	# 解析诗词详情页内容
	def poemDetail(self, response):
		
		poem_html = response.text.replace('<br/>','/n').replace('<strong>','').replace('</strong>','')
		poem_BS = BeautifulSoup(poem_html,'lxml')

		# 获取所有的内容板块，删除后三个猜你喜欢
		div_all_sons = poem_BS.find_all('div', class_='sons')[:-3]
		poem_BS_basecontent= div_all_sons[0]

		# 诗的题目
		poem_title = poem_BS_basecontent.find('h1').contents[0]
		print poem_title
		
		# 诗所在朝代时期,作者
		poem_dynasty_author = poem_BS_basecontent.find('p', class_ = 'source').find_all('a')
		for i in poem_dynasty_author:
			print i.contents[0]

		# 诗的内容
		poem_content_BS = poem_BS_basecontent.find('div',class_ = 'contson')
		# self.poemContentReduce(poem_content_BS)
		temp_poem_str = ''
		for i in poem_content_BS.descendants:
			if i.string != None:
				temp_poem_str = temp_poem_str + i.string
		
		print temp_poem_str	

		# 赞
		print list(poem_BS_basecontent.find('div',class_='good').descendants)[-1].strip()

		# 诗的译文,注释
		# https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx?id=2917
		for index in xrange(1,len(all_sons)):
			for child in all_sons[index].descendants:
				if child.name == 'h2':
					print child
		print '***************'


		# children = poem_content_BS.children
		# if children == None:
		# 	print poem_content_BS.contents[0]
		# else: 
		# 	for i in poem_content_BS.children:
		# 		print i


		# # 诗的题目
  #   	poem_title = scrapy.Field()
  #   	# 诗所在朝代时期
  #   	poem_dynasty = scrapy.Field()
  #   	# 诗的作者
  #   	poem_author = scrapy.Field()
  #   	# 诗的内容
  #   	poem_content = scrapy.Field()
  #   	# 诗的译文
  #   	poem_translation = scrapy.Field()
  #   	# 诗的注释
  #   	poem_annotation = scrapy.Field()
  #   	# 诗的赏析
  #   	poem_appreciate_analyze = scrapy.Field()
  #   	# 诗的参考资料
  #   	poem_appreciate_analyze_reference = scrapy.Field()
  #   	poem_translation_annotation_reference = scrapy.Field()
