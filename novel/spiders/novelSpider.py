# -*- coding: utf-8 -*-
import scrapy
from ..items import NovelItem


class NovelSpider(scrapy.Spider):
    name = "novelSpider"
    allowed_domains = ["2bgif.com"]
    start_urls = ['http://2bgif.com/novels']

    def parse(self, response):
        novelList = response.xpath('//ul[@class="bookshelf"]/li')[0]
        for novel in novelList:
            # 每个循环实例化一个item,并传给下面两个回调函数
            item = NovelItem()
            item['name'] = novelList.xpath('a[1]/img/@alt').extract_first()
            item['url'] = novelList.xpath('a[1]/@href').extract_first()

            yield scrapy.Request(url=response.urljoin(item['url']),
                                callback=self.parse_novel_summary,meta={'item':item})

        nextPage = response.xpath('//li[@class="mobile"]/a')
        # 遍历整个书架
        for next in nextPage:
            if next.xpath('span/text()').extract_first() == '下一页':
                nextPage = next.xpath('@href').extract_first()
                print(nextPage)
                yield scrapy.Request(url=response.urljoin(nextPage),
                                     callback=self.parse)

    def parse_novel_summary(self,response):
        item = response.meta['item']
        item['summary'] = response.xpath('//div[@id="description"]/text()').extract_first().strip()
        item['author'] = response.xpath('//div[@id="author-resume"]/text()').extract_first()
        firstPage = response.xpath('//table[@class="table table-bordered"]//a/@href').extract_first()

        novelFileName = (item['name'] + ('.txt'))
        with open(novelFileName, 'w') as f:
            f.write(item['summary'])
            f.write('\n')
            f.write(item['author'])
            f.write('\n' * 3)
        yield scrapy.Request(url=response.urljoin(firstPage),callback=self.parse_novel_content,
                                 meta={'item':item})


    def parse_novel_content(self,response):
        item = response.meta['item']
        item['content'] += response.xpath('//p[@id="content"]/text()').extract()
        item['content'] = '\n'.join(item['content'])

        nextPage = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # 遍历整本书
        if nextPage is not None:
            # print(item['name']+'----->loading new page')
            yield scrapy.Request(url=response.urljoin(nextPage),callback=self.parse_novel_content,
                                 meta={'item':item})

        # 写入txt文件中
        novelFileName = (item['name'] + ('.txt'))
        with open(novelFileName, 'a') as f:
            f.write('--newchapter--')
            f.write(item['content'])
        print(item['name'] + '----------------------->new page loading ')

        yield item

