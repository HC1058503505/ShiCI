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
        


