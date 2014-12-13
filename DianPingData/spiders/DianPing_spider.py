import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from DianPingData.items import DianpingdataItem,DianPingTag
from scrapy.http import Request
from scrapy.utils.url import unicode_to_str,safe_url_string
from urlparse import urljoin
import time

class DianPingDataSpider(scrapy.Spider):
    name = 'DianPing'
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://www.dianping.com/citylist"
    ]

    def parse(self, response):

        items = []
        sel = Selector(response)

        citySites = sel.xpath('//div/ul[@id="divArea"]')

        # zhixia city
        zhixiaCitys = citySites.xpath('li[1]/div')
        zhixiaNames = zhixiaCitys.xpath('a/strong/text()').extract()
        zhixiaUrls = zhixiaCitys.xpath('a/@href').extract()

        zhixiaCityLength = len(zhixiaNames)
        for i in range(0, zhixiaCityLength):
            item = DianpingdataItem()
            item['link'] = urljoin('http://www.dianping.com/',zhixiaUrls[i])
            item['title'] = unicode_to_str(zhixiaNames[i],'gb2312')
            items.append(item)



        #other city

        citys = citySites.xpath('li[@class="root"]/dl/dd')

        citysNames = citys.xpath('a/text()').extract()
        citysUrls = citys.xpath('a/@href').extract()

        cityLength = len(citysNames)
        print cityLength

        for j in range(0, cityLength):
            item = DianpingdataItem()
            item['link'] = urljoin('http://www.dianping.com/', citysUrls[j])
            item['title'] = unicode_to_str(citysNames[j],'gb2312')
            items.append(item)

        del items[1:len(items)]

        for item in items:
            yield Request(item['link'], meta={'item':item}, callback=self.parseCityLink)



            # yield Request(item['link'], meta={'item':item}, callback=self.parseCityLink)





    def parseCityLink(self, response):
        citysel = Selector(response)

        tagSites = citysel.xpath('//div/ul[@id="index-nav"]/li/div/a[@data-key>0]')

        items = []

        tag = tagSites.xpath('text()').extract()
        url = tagSites.xpath('@href').extract()

        tagLength = len(tag)
        for i in range(0, tagLength):
            item = DianPingTag()
            item['url'] = urljoin('http://www.dianping.com', url[i])
            item['tag'] = unicode_to_str(tag[i],'gb2312')
            items.append(item)


        del items[1:len(items)]
        print items

        for item in items:
            time.sleep(2)
            yield Request(item['url'], meta={'item':item}, callback=self.parseTagUrl)


    def parseTagUrl(self, response):

        shopSel = Selector(response)
        shopSites = shopSel.xpath('//div[@class="shop-wrap"]/ul/li/div[@class="tit"]')

        print shopSites
        titles = shopSites.xpath('a[@data-hippo-type="shop"]/@title')
        urls = shopSites.xpath('a[@data-hippo-type="shop"]/@href')

        print urls

        items = []


