# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import re

from datetime import datetime

class BaiduPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        return item


# class BaiduPipeline(object):
#     def process_item(self, item, spider):
#         if re.search(r"([0-9]+),", item["text"]):
#             pattern = re.search(r"([0-9]+),", item["text"]).group()
#             rep = ",,".join(pattern.split(","))
#             item["text"] = re.sub(pattern, rep, item["text"])
#         else:
#             pass
#         return item

#     def open_spider(self, item, spider):
#         pass

#     def close_spider(self, item, spider):
#         return "爬取结束"
