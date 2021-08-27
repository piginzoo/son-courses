# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import os

logger = logging.getLogger(__name__)


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        filename = item['name']
        title = item['title']

        if not os.path.exists("data/"):
            os.makedirs("data")

        with open(os.path.join("data/", filename), "w",encoding="utf-8") as f:
            f.write(title)
            f.write("\n")
            f.write(item['content'])
            logger.info('爬取了文件：%s', filename)
