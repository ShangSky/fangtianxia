# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from danke_spider import DanKe


class FangSpider(CrawlSpider):
    name = 'fang'
    allowed_domains = ['zu.fang.com']
    start_urls = [
        'http://zu.fang.com/house/a21-n31/',
        'http://sh.zu.fang.com/house/a21-n31/',
        'http://hz.zu.fang.com/house/a21-n31/',
        'http://tj.zu.fang.com/house/a21-n31/',
        'http://sz.zu.fang.com/house/a21-n31/',
        'http://gz.zu.fang.com/house/a21-n31/',
        'http://wuhan.zu.fang.com/house/a21-n31/',
        'http://nanjing.zu.fang.com/house/a21-n31/',
        'http://cd.zu.fang.com/house/a21-n31/'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'http://zu\.fang\.com/house/a21-i3\d+-n31/'), follow=True),
        Rule(LinkExtractor(allow=r'http://(sh|hz|tj|sz|gz|wuhan|nanjing|cd)\.zu\.fang\.com/house/a21-i3\d+-n31/'), follow=True),
        Rule(LinkExtractor(allow=r'http://(sh|hz|tj|sz|gz|wuhan|nanjing|cd)\.zu\.fang\.com/chuzu/1_\d+_-1\.htm'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'zu\.fang\.com/chuzu/1_\d+_-1\.htm'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = {}
        item['city'] = response.xpath('//div[@class="newnav20141104nr"]//div[@class="s4Box"]/a/text()').extract_first() + '市'
        item['xiaoqu'] = response.xpath('//span[@class="zf_xqname"]/text()').extract_first()
        item['phone'] = response.xpath('//span[@class="zf_mftel"]/text()').extract_first()
        item['doorplate'] = item['xiaoqu']

        if item['phone'] is None:
            return
        if '-'not in item['phone']:
            print(item)
            danke = DanKe()
            danke.run(item)
