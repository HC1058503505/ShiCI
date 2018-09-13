
# -*- coding:utf-8 -*-

import re
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from ShiCi.items import BookCatalogueItem
import time
import json

class BookCatalogueSpider(scrapy.Spider):
	
	name = 'bookcatalogue'
	allowed_domains = ['gushiwen.org']
	bash_url = 'https://so.gushiwen.org/guwen/'

	def start_requests(self):
		# 古籍不限
		yield Request(self.bash_url, self.parase)


	def parase(self, response):
		book_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		book_bs = BeautifulSoup(book_html, 'lxml')
		book_bs_main3 = book_bs.find('div', class_ = 'main3')
		book_bs_main3_title_type = book_bs_main3.find('div', class_='titletype')
		book_bs_main3_title_type_son2 = book_bs_main3_title_type.find_all('div', class_='son2')


		for div in book_bs_main3_title_type_son2:
			book_bs_main3_title_type_son2_left = div.find('div',class_='sleft')
			# 大分类
			book_category = book_bs_main3_title_type_son2_left.get_text().split(u'：')[0]

			book_bs_main3_title_type_son2_right = div.find('div',class_='sright')
			book_bs_main3_title_type_son2_right_a = book_bs_main3_title_type_son2_right.find_all('a')

			for a in book_bs_main3_title_type_son2_right_a:
				# 小分类
				book_sub_category = a.string
				# 每个小分类对应的url
				book_catalogue_url = 'https://so.gushiwen.org' + a['href']
				yield Request(book_catalogue_url, self.bookList, meta={'book_category' : book_category, 'book_sub_category' : book_sub_category})
				



	def bookList(self, response):

		book_catalogues = []

		book_list_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		book_list_bs = BeautifulSoup(book_list_html,'lxml')
		book_list_div_main3 = book_list_bs.find('div',class_='main3')
		book_list_page_div = book_list_div_main3.find('div',class_='son1')
		book_list_page_span = book_list_page_div.find('span')
		page_span_split_list = book_list_page_span.string.split('/')
		page_span = page_span_split_list[-1]
		page = int(re.findall('\d+',page_span)[0])
		book_category = response.meta['book_category']
		book_sub_category = response.meta['book_sub_category']

		if page == 1:
			book_list_div_main3_sonspic = book_list_div_main3.find_all('div',class_='sonspic')
			for sonspic in book_list_div_main3_sonspic:

				book_catalogue_item = BookCatalogueItem()
				book_catalogue_item['book_category'] = book_category
				book_catalogue_item['book_sub_category'] = book_sub_category
				book_divimg = sonspic.find('div',class_='divimg')
				book_divimg_a = book_divimg.a
				book_divimg_a_href = book_divimg_a['href']
				book_divimg_a_href = book_divimg_a_href.split('_')[-1]
				book_divimg_a_id = book_divimg_a_href.split('.')[0]

				book_catalogue_item['book_id'] = book_divimg_a_id

				book_catalogues.append(book_catalogue_item)
		else:
			# 大分类中小分类的每页内容
			for page_num in xrange(2,page+1):
				url = 'https://so.gushiwen.org/guwen/Default.aspx?p=' + str(page_num) + '&c=' + book_sub_category
				# yield Request(url,self.bookDetail, meta={'book_category' : book_category, 'book_sub_category' : book_sub_category})
				new_response = requests.get(url)
				time.sleep(1)
				book_html = new_response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
				book_bs = BeautifulSoup(book_html, 'lxml')
				book_div_main3 = book_bs.find('div',class_='main3')

				if book_div_main3 == None:
					print 'book_content_bs-----start'
					print book_bs
					print 'book_content_bs-----end'
					continue
				book_div_main3_sonspic = book_div_main3.find_all('div',class_='sonspic')
				for sonspic in book_div_main3_sonspic:

					book_catalogue_item = BookCatalogueItem()
					book_catalogue_item['book_category'] = book_category
					book_catalogue_item['book_sub_category'] = book_sub_category
					book_divimg = sonspic.find('div',class_='divimg')
					book_divimg_a = book_divimg.a
					book_divimg_a_href = book_divimg_a['href']
					book_divimg_a_href = book_divimg_a_href.split('_')[-1]
					book_divimg_a_id = book_divimg_a_href.split('.')[0]

					book_catalogue_item['book_id'] = book_divimg_a_id

					book_catalogues.append(book_catalogue_item)

		return book_catalogues

	# def bookDetail(self, response):
	# 	book_catalogues = []
	# 	book_list_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
	# 	book_list_bs = BeautifulSoup(book_list_html,'lxml')
	# 	book_list_div_main3 = book_list_bs.find('div',class_='main3')
	# 	book_list_div_main3_sonspic = book_list_div_main3.find_all('div',class_='sonspic')
	# 	book_category = response.meta['book_category']
	# 	book_sub_category = response.meta['book_sub_category']
	# 	for sonspic in book_list_div_main3_sonspic:

	# 		book_catalogue_item = BookCatalogueItem()
	# 		book_catalogue_item['book_category'] = book_category
	# 		book_catalogue_item['book_sub_category'] = book_sub_category
	# 		book_divimg = sonspic.find('div',class_='divimg')
	# 		book_divimg_a = book_divimg.a
	# 		book_divimg_a_href = book_divimg_a['href']
	# 		book_divimg_a_href = book_divimg_a_href.split('_')[-1]
	# 		book_divimg_a_id = book_divimg_a_href.split('.')[0]

	# 		book_catalogue_item['book_id'] = book_divimg_a_id

	# 		book_catalogues.append(book_catalogue_item)

	# 	return book_catalogues





	



























