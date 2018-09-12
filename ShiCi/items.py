# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShiciItem(scrapy.Item):
    # define the fields for your item here like:

    poem_id = scrapy.Field()

    # 诗的题目
    poem_title = scrapy.Field()

    # 诗所在朝代时期
    poem_dynasty = scrapy.Field()

    # 诗的作者
    poem_author = scrapy.Field()

    # 诗的内容
    poem_content = scrapy.Field()

    # 诗的标签
    poem_tags = scrapy.Field()

    # 赞
    poem_praise_count = scrapy.Field()

    # 诗的注释翻译，背景故事，参考资料
    poem_extension = scrapy.Field()


class PoetItem(scrapy.Item):
    # 诗人id标识
    poet_id = scrapy.Field()

    # 诗人朝代
    poet_dynasty = scrapy.Field()

    # 诗人名字
    poet_name = scrapy.Field()

    # 诗人画像
    poet_portrait = scrapy.Field()

    # 诗人简介
    poet_abstract = scrapy.Field()

    # 诗人事迹
    poet_extension = scrapy.Field()
        


class SentenceItem(scrapy.Item):
    
    # 诗句类型
    sentence_type = scrapy.Field()

    # 诗句内容
    sentence_content = scrapy.Field()

    # 诗句id
    sentence_id = scrapy.Field()

    # 诗句所属诗名
    sentence_poem_title = scrapy.Field()

    # 诗句所属诗人
    sentence_poem_author = scrapy.Field()

    # 诗句所属诗id
    sentence_poem_id = scrapy.Field()


class BookItem(scrapy.Item):
    # 估计id
    book_id = scrapy.Field()
    # bookimg
    book_img = scrapy.Field()
    # 古籍大纲
    book_outline = scrapy.Field()
    # 古籍目录
    book_catalogue = scrapy.Field()
    # 古籍名
    book_name = scrapy.Field()
    # 古籍章节内容
    book_contents = scrapy.Field()
    # 古籍更改
    book_abstract = scrapy.Field()
        
        