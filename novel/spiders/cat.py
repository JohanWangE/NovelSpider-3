# -*- coding: utf-8 -*-
import scrapy
from ..items import CatPicItem

class CatSpider(scrapy.Spider):
    name = "cat"
    start_urls = ['https://pixabay.com/zh/photos/?q=cat&image_type=&cat=&min_width=&min_height=']

    def parse(self, response):
        pic_grid = response.xpath('//div[@id="photo_grid"]/div[@class="item"]')
        for pic in pic_grid:
            item = CatPicItem()
            url = pic.xpath('a[1]/img')
            if url.xpath('@data-lazy').extract_first() is not None:
                img = url.xpath('@data-lazy').extract_first()
            else:
                img = url.xpath('@src').extract_first()
            item['picUrl'] = img
            yield item

        newPage = response.xpath('//a[@style="display:block;margin:50px auto;max-width:240px"]'
                                 '/@href').extract_first()
        print(response.urljoin(newPage))
        if newPage is not None:
            yield scrapy.Request(url=response.urljoin(newPage),callback=self.parse,
                                 meta={'item':item})