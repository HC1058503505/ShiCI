
# -*- coding:utf-8 -*-

import re
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from ShiCi.items import ShiciItem
import json
import time
class PoemSpider(scrapy.Spider):
	"""docstring for PoemSpider"""
	
	name = 'poem'
	allowed_domains = ['gushiwen.org']
	bash_url = 'https://www.gushiwen.org/shiwen/'
	bashurl = '.aspx'

	# 开始爬取，获取诗词详情页url
	def start_requests(self):
		for i in xrange(1,1001):
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
			poem_id_aspx = url.split('_')[-1]
			poem_id = poem_id_aspx.split('.')[0]
			yield Request(url, self.poemDetail,meta={'poem_id': poem_id})
		


	# 解析诗词详情页内容
	def poemDetail(self, response):
		poem_item = ShiciItem()

		poem_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		poem_BS = BeautifulSoup(poem_html,'lxml')

		# 获取所有的内容板块，删除后三个猜你喜欢
		div_all_sons = poem_BS.find_all('div', class_='sons')
		poem_BS_basecontent= div_all_sons[0]

		# poemid
		poem_item['poem_id'] = response.meta['poem_id']
		# 诗的题目
		poem_title = poem_BS_basecontent.find('h1').contents[0]
		poem_item['poem_title'] = poem_title
		
		# 诗所在朝代时期,作者
		poem_dynasty_author = poem_BS_basecontent.find('p', class_ = 'source').get_text().split(u'：')
		poem_item['poem_dynasty'] = poem_dynasty_author[0]
		poem_item['poem_author'] = poem_dynasty_author[-1]

		# 诗的内容
		poem_content_BS = poem_BS_basecontent.find('div',class_ = 'contson')
		poem_content = poem_content_BS.get_text('/n',strip=True)
		poem_content = '  ' + poem_content
		poem_content = poem_content.replace('/n', '/n  ')
		poem_item['poem_content'] = poem_content

		# 诗的标签
		poem_tags_div = poem_BS_basecontent.find('div', class_ = 'tag')
		if poem_tags_div == None:
			poem_item['poem_tags'] = []
		else:
			poem_item['poem_tags'] = poem_tags_div.get_text('|',strip=True).split('|')
		
		# 赞
		poem_praise_count = list(poem_BS_basecontent.find('div',class_='good').descendants)[-1].strip()
		poem_item['poem_praise_count'] = poem_praise_count

		poem_extension = []
		# 诗的译文,注释
		# https://so.gushiwen.org/shiwen2017/ajaxshangxi.aspx?id=2917
		for index in xrange(1,len(div_all_sons)):
			son = div_all_sons[index]
			
			if son.find('div', class_='contyishang') == None:
				continue
			
			extension_bs = son
			if son.attrs.has_key('id'):
				son_id = son['id']
				
				son_identifier = re.findall('\d+',son_id)[0]
				son_type = ''.join(re.findall('[a-zA-Z]',son_id))
				ajax_url ='https://so.gushiwen.org/shiwen2017/ajax' + son_type + '.aspx?id=' + son_identifier
				extension_ajax = requests.get(ajax_url)
				time.sleep(1)
				extension_ajax_text = extension_ajax.text.replace('<br />', '/n')
				extension_bs = BeautifulSoup(extension_ajax_text,'lxml')
				
			extension_bs_contyishang = extension_bs.find('div','contyishang')
			if extension_bs_contyishang == None:
				continue
			else:
				# h2
				extension_bs_h2 = extension_bs.find('h2')
				extension_title = extension_bs_h2.get_text()

			# dingpai
			dingpai_div = extension_bs.find('div', class_='dingpai')
			dingpai_text = dingpai_div.get_text('|',strip=True).split('|')
			extension_good = re.findall('\d+',dingpai_text[0])[0]
			extension_bad = re.findall('\d+',dingpai_text[1])[0]

			# cankao_div = extension_bs.find('div', class_='cankao')
			# cankao
			# cankao_text = cankao_div.get_text('',strip=True)

			# cankao_div.decompose()
			
			extension_bs_contyishang = extension_bs.find('div',class_='contyishang')
			if extension_bs_contyishang != None:
				son_extension_p = extension_bs.find_all('p')
				if son_extension_p == None or len(son_extension_p) == 0:
					if extension_bs_h2 != None:
						extension_bs_h2.decompose()
						extension_bs_p_str = extension_bs_contyishang.get_text(strip=True)
					else:
						pass
				else:

					# extension content
					extension_bs_p_str = ''
					for p in son_extension_p:
						extension_bs_p_str = extension_bs_p_str + p.get_text(strip=True) + '/n'
			else:
				pass


			temp_extension = {
				'extension_title' : extension_title,
				'extension_good' : extension_good,
				'extension_bad' : extension_bad,
				'extension_content' : extension_bs_p_str
			} 

			poem_extension.append(temp_extension)


		poem_item['poem_extension'] = poem_extension

		return  poem_item

















