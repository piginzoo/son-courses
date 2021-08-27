import logging

import scrapy
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

url_confs = [
    {
        'type': '校园新闻',
        'pattern': 'http://www.bjcjl.net/xyxw/index_{}.html',
        'num': 50
    }]


class P2pSpider(scrapy.Spider):
    name = "chenjinglun"

    def __get_urls(self):
        urls = []
        for url_conf in url_confs:

            url = {}
            url['type'] = url_conf['type']
            # 处理2->结尾的其他的列表页
            for i in range(1, url_conf['num'] + 1):
                url = {}
                url['type'] = url_conf['type']
                url['url'] = url_conf['pattern'].format(i)
                urls.append(url)
                logger.debug("解析出列表：%s", url['url'])
        return urls

    def start_requests(self):

        for url in self.__get_urls():
            logger.debug("URL是：%s", url['url'])
            yield scrapy.Request(
                url=url['url'],
                callback=self.parse,
                meta={'type': url['type']}
            )

    def parse_item(self, response):
        type = response.meta['type']
        item = {}

        # 用css选择器抽取标题
        title = response.css('.detail_tit h3::text').extract()
        logger.debug("文章标题：%s", title)

        # 用css选择器抽取内容
        content = response.css('.TRS_Editor').extract()
        logger.debug("文章内容：[%s...]", title[:20])

        # 用BeautifulSoup清除html标签
        bf = BeautifulSoup(content[0])

        filename = response.url.split("/")[-1]

        item['content'] = bf.get_text()
        item['title'] = title[0]
        item['name'] = type + "-" + filename

        return item

    # 这个parse既要解析每个列表页，然后得到列表页中的每个文章的链接
    # 然后通过yield将这些链接返回，并制定解析这些内容链接的额函数为parse_item
    def parse(self, response):

        website = response.url[:response.url.rfind("/")]

        links = response.css('.detail_list_box li a::attr(href)').extract()
        logger.debug("列表URL：%s", links)
        for _link in links:
            if _link.find(".html") == -1:
                logger.warning("不是html结尾的列表URL：%s", _link)
                continue

            _link = _link[1:]  # 去掉"./xxx/xxx.html"的第一个点
            logger.debug("爬取内容URL：website：%s,_link:%s", website, _link)
            _link = website + _link
            logger.debug("爬取内容URL：%s", _link)

            yield scrapy.Request(
                url=_link,
                callback=self.parse_item,
                meta={'type': response.meta['type']}  # 这里要传递一下从link传过来的类型type
            )
