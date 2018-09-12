
# -*- coding:utf-8 -*-

import re
import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from ShiCi.items import BookItem
import time
import json

class BookItem(scrapy.Spider):
	
	name = 'book'
	allowed_domains = ['gushiwen.org']
	bash_url = 'https://so.gushiwen.org/guwen/'

	def start_requests(self):
		yield Request(self.bash_url, self.parase)

	def parase(self, response):
		book_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		book_bs = BeautifulSoup(book_html, 'lxml')
		book_bs_main3 = book_bs.find('div', class_ = 'main3')
		book_bs_main3_title_type = book_bs_main3.find('div', class_='titletype')
		book_bs_main3_title_type_son2 = book_bs_main3_title_type.find_all('div', class_='son2')

		for div in book_bs_main3_title_type_son2:
			book_bs_main3_title_type_son2_left = div.find('div',class_='sleft')
			book_outline = book_bs_main3_title_type_son2_left.get_text().split(u'：')[0]

			book_bs_main3_title_type_son2_right = div.find('div',class_='sright')
			book_bs_main3_title_type_son2_right_a = book_bs_main3_title_type_son2_right.find_all('a')
			for a in book_bs_main3_title_type_son2_right_a:
				book_catalogue = a.string
				book_catalogue_url = 'https://so.gushiwen.org' + a['href']
				yield Request(book_catalogue_url, self.bookList, meta={'book_outline' : book_outline, 'book_catalogue' : book_catalogue})



	def bookList(self, response):
		book_list_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		book_list_bs = BeautifulSoup(book_list_html,'lxml')
		book_list_div_main3 = book_list_bs.find('div',class_='main3')
		book_list_page_div = book_list_div_main3.find('div',class_='son1')
		book_list_page_span = book_list_page_div.find('span')
		page_span_split_list = book_list_page_span.string.split('/')
		page_span = page_span_split_list[-1]
		page = int(re.findall('\d+',page_span)[0])

		book_outline = response.meta['book_outline']
		book_catalogue = response.meta['book_catalogue']
		for page_num in xrange(1,page+1):
			url = 'https://so.gushiwen.org/guwen/Default.aspx?p=' + str(page_num) + '&c=' + book_catalogue
			yield Request(url,self.bookDetail, meta={'book_outline' : book_outline, 'book_catalogue' : book_catalogue})



	def bookDetail(self, response):
		book_list_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		book_list_bs = BeautifulSoup(book_list_html,'lxml')
		book_list_div_main3 = book_list_bs.find('div',class_='main3')
		book_list_div_main3_sonspic = book_list_div_main3.find_all('div',class_='sonspic')


		for sonspic in book_list_div_main3_sonspic:

			book_divimg = sonspic.find('div',class_='divimg')
			book_divimg_a = book_divimg.a
			book_divimg_a_href = book_divimg_a['href']
			book_divimg_a_href = book_divimg_a_href.split('_')[-1]
			book_divimg_a_id = book_divimg_a_href.split('.')[0]

			book_href = 'https://so.gushiwen.org' + book_divimg_a['href']
			book_outline = response.meta['book_outline']
			book_catalogue = response.meta['book_catalogue']
			yield Request(book_href, self.book,meta={'book_outline' : book_outline, 'book_catalogue' : book_catalogue,'book_id' : book_divimg_a_id})
		# book_divimg_img = book_divimg.find('img')
		# book_img = book_divimg_img['href']
		# book_name = book_divimg_img['alt']


	def book(self, response):

		book_outline = response.meta['book_outline']
		book_catalogue = response.meta['book_catalogue']
		book_id = response.meta['book_id']

		book_item = BookItem()
		book_item['book_outline'] = book_outline
		book_item['book_catalogue'] = book_catalogue
		book_item['book_id'] = book_id


		book_list_html = response.text.replace('<br />','/n').replace('<strong>','').replace('</strong>','')
		book_list_bs = BeautifulSoup(book_list_html,'lxml')
		book_list_div_main3 = book_list_bs.find('div',class_='main3')
		book_list_div_main3_sonspic = book_list_div_main3.find('div',class_='sonspic')

		book_div_cont = book_list_div_main3_sonspic.find('div',class_='cont')


		book_divimg = book_div_cont.find('div',class_='divimg')
		book_divimg_img = book_divimg.find('img')
		book_img = book_divimg_img['src']
		book_name = book_divimg_img['alt']

		book_item['book_name'] = book_name
		book_item['book_img'] = book_img

		book_divimg.decompose()

		book_abstract = book_div_cont.get_text(strip=True)
		# book_item['book_abstract'] = book_abstract
		book_list_div_main3_sons = book_list_div_main3.find('div',class_='sons')
		book_list_div_bookcont = book_list_div_main3_sons.find_all('div',class_='bookcont')

		book_contents = []

		for bookcont in book_list_div_bookcont:
			bookcont_bookMl = bookcont.find('div',class_='bookMl')
			if bookcont_bookMl == None:
				book_sub_title = ''
				bookcont_ul = bookcont.find('ul')
				bookcont_a = bookcont_ul.find_all('a')
			else:
				book_sub_title = bookcont_bookMl.get_text()
				bookcont_a = bookcont.find_all('a')
			

			for a in bookcont_a:
					bookcont_a_string = a.string

					if a['href'] == None:
						book_content = ''
					else:
						bookcont_a_href = 'https://so.gushiwen.org' + a['href']
						book_content_response = requests.get(bookcont_a_href)
						book_content_text = book_content_response.text.replace('<br />', '/n')
						book_content_bs = BeautifulSoup(book_content_text, 'lxml')
						book_content_bs_main3 = book_content_bs.find('div',class_='main3')
						book_content_bs_main3_cont = book_content_bs_main3.find('div',class_='cont')
						book_content_bs_main3_cont.h1.decompose()
						book_content = book_content_bs_main3_cont.get_text('/n',strip=True)


					book_content_temp = {
						'book_chapter_section' : book_sub_title,
						'book_chapter_title' : bookcont_a_string,
						'book_chapter_content' : book_content
					}

					book_contents.append(book_content_temp)


		book_item['book_contents'] = book_contents


		return book_item



























