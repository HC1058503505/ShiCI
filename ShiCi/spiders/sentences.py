# -*- coding:utf-8 -*-

import re
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from ShiCi.items import SentenceItem
import time
import json

class SentencesSpider(scrapy.Spider):
	
	name = 'sentences'
	allowed_domains = ['gushiwen.org']
	bash_url = 'https://so.gushiwen.org/mingju'

	def start_requests(self):
		yield Request(self.bash_url, self.parse)

	def parse(self, response):
		sentences_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		sentences_bs = BeautifulSoup(sentences_html,'lxml')		
		sright_div = sentences_bs.find('div',class_='sright')
		sright_div_a = sright_div.find_all('a')
		for a in sright_div_a:
			sentences_type = a.string
			sentences_href = 'https://so.gushiwen.org' + a['href']
			yield Request(sentences_href, self.sentencesList, meta={'sentences_type' : sentences_type})

	def sentencesList(self, response):
		sentences_list_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		sentences_list_bs = BeautifulSoup(sentences_list_html,'lxml')
		sentences_list_div_main3 = sentences_list_bs.find('div',class_='main3')
		sentences_list_page_div = sentences_list_div_main3.find('div',class_='son1')
		sentences_list_page_span = sentences_list_page_div.find('span')
		page_span_split_list = sentences_list_page_span.string.split('/')
		page_span = page_span_split_list[-1]
		page = int(re.findall('\d+',page_span)[0])

		sentences_type = response.meta['sentences_type']
		for page_num in xrange(1,page+1):
			url = 'https://so.gushiwen.org/mingju/Default.aspx?p=' + str(page_num) + '&c=' + sentences_type
			yield Request(url,self.sentences, meta={'sentences_type' : sentences_type})

	def sentences(self, response):

		items = []

		sentences_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		sentences_bs = BeautifulSoup(sentences_html,'lxml')
		sentences_bs_main3 = sentences_bs.find('div',class_='main3')
		sentences_bs_left = sentences_bs_main3.find('div',class_='left')
		sentences_bs_left_sons = sentences_bs_left.find('div',class_='sons')
		sentences_bs_left_sons_div = sentences_bs_left_sons.find_all('div',class_='cont')
		sentences_type = response.meta['sentences_type']

		for div in sentences_bs_left_sons_div:

			sentenceItem = SentenceItem()
			sentenceItem['sentence_type'] = sentences_type

			div_a = div.find_all('a')
			div_a_sentence_tag = div_a[0]
			div_a_sentence = div_a_sentence_tag.string
			div_a_sentence_href = div_a_sentence_tag['href']

			div_a_sentence_id = div_a_sentence_href.split('_')
			div_a_sentence_id = div_a_sentence_id[-1]
			div_a_sentence_id = div_a_sentence_id.split('.')
			div_a_sentence_id = div_a_sentence_id[0]

			sentenceItem['sentence_content'] = div_a_sentence
			sentenceItem['sentence_id'] = div_a_sentence_id

			div_a_poem_tag = div_a[-1]
			div_a_poem = div_a_poem_tag.string
			div_a_poem_author_title = div_a_poem.split(u'《')
			div_a_poem_author = div_a_poem_author_title[0]
			div_a_peom_title = u'《' + div_a_poem_author_title[-1]

			sentenceItem['sentence_poem_title'] = div_a_peom_title
			sentenceItem['sentence_poem_author'] = div_a_poem_author

			div_a_poem_href = div_a_poem_tag['href']

			div_a_poem_id = div_a_poem_href.split('_')
			div_a_poem_id = div_a_poem_id[-1]
			div_a_poem_id = div_a_poem_id.split('.')
			div_a_poem_id = div_a_poem_id[0]
			sentenceItem['sentence_poem_id'] = div_a_poem_id

			items.append(sentenceItem)


		return items
