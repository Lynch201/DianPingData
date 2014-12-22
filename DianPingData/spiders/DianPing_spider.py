# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from DianPingData.items import DianPingTag,ShopDetail
from scrapy.http import Request
from scrapy.utils.url import unicode_to_str,safe_url_string
from urlparse import urljoin
import re
import json
import time

lnglatPa = re.compile(r'\({.*}\)')
rootUrl = 'http://www.dianping.com/'
browAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 ' \
            'Safari/537.36'
# browAgent = 'your agent string'

class CitySpider(scrapy.Spider):
    name = 'CrawlCity'
    RANDOMIZE_DOWNLOAD_DELAY = True
    download_delay = 4
    allowed_domains = ["dianping.com"]

    def __init__(self, city=None, *args, **kwargs):
        super(CitySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.dianping.com/%s' % city]

    def parse(self, response):

        # ###################################
        #
        # 进入城市的标签页
        #
        # ###################################
        citysel = Selector(response)
        tags = citysel.xpath('//div/ul[@id="index-nav"]/li')
        tagslen = len(tags)

        # ###################################
        #
        # 进入标签
        #
        # ###################################
        for i in range(0, tagslen):
        # for i in range(0, 1):
            tagsi = citysel.xpath('//div/ul[@id="index-nav"]/li[' + str(i + 1) + ']')

            names = tagsi.xpath('a[@class="name"]/span/text()').extract()
            bigtagName = unicode_to_str(names[0], 'utf-8').strip()

            smallTags = tagsi.xpath('div/a[@data-key>0]')
            tag = smallTags.xpath('text()').extract()
            url = smallTags.xpath('@href').extract()

            tagLength = len(tag)


            # ###################################
            #
            # 进入子标签
            #
            # ###################################

            for j in range(0, tagLength):
            # for j in range(0, 1):
                tags = {}
                tags['bigtag'] = unicode(bigtagName, 'utf-8')
                tags['smalltag'] = unicode(unicode_to_str(tag[j], 'utf-8').strip(), 'utf-8')
                urlto = urljoin(rootUrl, url[j])
                yield Request(urlto, headers={'User-Agent': browAgent},
                              meta={'tag':tags}, callback=self.parseTagUrl)

    def parseTagUrl(self, response):

        tags = response.meta['tag']
        shopSel = Selector(response)
        shopSites = shopSel.xpath('//div/ul/li/div[@class="txt"]/div[@class="tit"]')

        titles = shopSites.xpath('a[@data-hippo-type="shop"]/@title').extract()
        urls = shopSites.xpath('a[@data-hippo-type="shop"]/@href').extract()

        listLen = len(titles)

        items = []
        links = []
        for i in range(0, listLen):

            item = ShopDetail()
            item['tag1'] = tags['bigtag']
            item['tag2'] = tags['smalltag']
            item['name'] = unicode(unicode_to_str(titles[i],'utf-8'), 'utf-8')
            item['link'] = urljoin(rootUrl, urls[i])
            links.append(urljoin(rootUrl, urls[i]))
            items.append(item)

        # del items[2:len(items)]

        itemsLen = len(items)

        for i in range(0, itemsLen):
            yield items[i]
            # yield  Request(links[i], headers={'User-Agent': browAgent},
            #               meta={'item':items[i]}, callback=self.parseShopDetail)

        nextpage = shopSel.xpath('//div[@class="page"]/a[@class="next"]/@href').extract()


        if len(nextpage) != 0:
            url = urljoin(rootUrl, nextpage[0])
            yield Request(url, headers={'User-Agent': browAgent},
                              meta={'tag':tags}, callback=self.parseTagUrl)







class DianPingDataSpider(scrapy.Spider):
    name = 'DianPing'
    download_delay = 4
    allowed_domains = ["dianping.com"]
    start_urls = [
        "http://www.dianping.com/citylist"
    ]

    def parse(self, response):

        items = []
        sel = Selector(response)

        citySites = sel.xpath('//div/ul[2][@id="divArea"]')

        # ###################################
        #
        # 直辖市
        #
        # ###################################
        zhixiaCitys = citySites.xpath('li[1]/div')
        zhixiaNames = zhixiaCitys.xpath('a/strong/text()').extract()
        zhixiaUrls = zhixiaCitys.xpath('a/@href').extract()

        zhixiaCityLength = len(zhixiaNames)
        for i in range(0, zhixiaCityLength):
            item = {}
            item['link'] = urljoin(rootUrl, zhixiaUrls[i])
            item['city'] = unicode(unicode_to_str(zhixiaNames[i],'utf-8'), 'utf-8')
            items.append(item)



        # ###################################
        #
        # 其他重要城市
        #
        # ###################################

        citys = citySites.xpath('li[@class="root"]/dl/dd')
        citysImport = citys.xpath('a/child::node()[local-name() = "strong"]/..')
        citysNames = citysImport.xpath('strong/text()').extract()
        citysUrls = citysImport.xpath('@href').extract()

        cityLength = len(citysNames)
        print cityLength

        for j in range(0, cityLength):
            item = {}
            item['link'] = urljoin(rootUrl, citysUrls[j])
            item['city'] = unicode(unicode_to_str(citysNames[j],'utf-8').strip(),'utf-8')
            #items.append(item)

        del items[1:len(items)]

        for item in items:
            # yield Request(item['link'], meta={'item':item}, callback=self.parseTag)
            yield Request(item['link'], meta={'city':item['city']},
                          headers={'User-Agent': browAgent}, callback=self.parseCity)

        # ###################################
        #
        # 其他城市（非黑提名字，主要是进入之后的菜单栏不同）
        #
        # ###################################
        citysUnImport = citys.xpath('a/child::node()[local-name() != "strong"]/..')
        citysUnImportNames = citysUnImport.xpath('text()').extract()
        citysUnImportUrls = citysUnImport.xpath('@href').extract()

        cityUnImportLength = len(citysUnImportNames)

        itemUnimport = []
        for i in range(0, cityUnImportLength):
            item = {}
            item['link'] = urljoin(rootUrl, citysUnImportUrls[i])
            item['city'] = unicode(unicode_to_str(citysUnImportNames[i],'utf-8').strip(),'utf-8')

            #itemUnimport.append(item)


        # del itemUnimport[1:len(itemUnimport)]

        for item1 in itemUnimport:
            # yield Request(item['link'], meta={'item':item}, callback=self.parseTag)
            yield Request(item1['link'], meta={'city':item1['city']},
                          headers={'User-Agent': browAgent}, callback=self.parseCityUnimport)

    def parseTag(self, response):
        citysel = Selector(response)

        tags = citysel.xpath('//div/ul[@id="index-nav"]/li')

        tagslen = len(tags)

        for i in range(0, tagslen):
            tagsi = citysel.xpath('//div/ul[@id="index-nav"]/li[' + str(i + 1) + ']')

            names = tagsi.xpath('a[@class="name"]/span/text()').extract()
            # print unicode_to_str(names[0], 'utf-8')

            bigtagName = unicode_to_str(names[0], 'utf-8')
            # TagDiv = tagsi.xpath('div[@class="secondary-category J-secondary-category"]')
            smallTags = tagsi.xpath('div/a[@data-key>0]/text()').extract()
            for smalltag in smallTags:
                print bigtagName, unicode_to_str(smalltag, 'utf-8')



    def parseCity(self, response):

        # ###################################
        #
        # 进入城市的标签页
        #
        # ###################################
        citysel = Selector(response)
        city = response.meta['city']
        tags = citysel.xpath('//div/ul[@id="index-nav"]/li')
        tagslen = len(tags)

        # ###################################
        #
        # 进入标签
        #
        # ###################################
        # for i in range(0, tagslen):
        for i in range(0, 1):
            tagsi = citysel.xpath('//div/ul[@id="index-nav"]/li[' + str(i + 1) + ']')

            names = tagsi.xpath('a[@class="name"]/span/text()').extract()
            bigtagName = unicode_to_str(names[0], 'utf-8').strip()

            smallTags = tagsi.xpath('div/a[@data-key>0]')
            tag = smallTags.xpath('text()').extract()
            url = smallTags.xpath('@href').extract()

            tagLength = len(tag)

			
            # ###################################
            #
            # 进入子标签
            #
            # ###################################

            # for j in range(0, tagLength):
            for j in range(0, 1):
                tags = {}
                tags['city'] = city
                tags['bigtag'] = unicode(bigtagName, 'utf-8')
                tags['smalltag'] = unicode(unicode_to_str(tag[j], 'utf-8').strip(), 'utf-8')
                urlto = urljoin(rootUrl, url[j])
                yield Request(urlto, headers={'User-Agent': browAgent},
                              meta={'tag':tags}, callback=self.parseTagUrl)


    def parseCityUnimport(self, response):

        # ###################################
        #
        # 进入城市的标签页
        #
        # ###################################
        citysel = Selector(response)
        city = response.meta['city']
        tags = citysel.xpath('//ul[@class="category-nav J-category-nav Hide"]/li')
        tagslen = len(tags)
        for i in range(0, tagslen):
        # for i in range(0, 1):
            tagsi = citysel.xpath('//ul[@class="category-nav J-category-nav Hide"]/li[' + str(i + 1) + ']')
            names = tagsi.xpath('a[@class="name"]/text()').extract()
            bigtagName = unicode_to_str(names[0], 'utf-8').strip()

            print 'bignames:' + bigtagName

            smallTags = tagsi.xpath('div/a[@data-key>0]')
            tag = smallTags.xpath('text()').extract()
            url = smallTags.xpath('@href').extract()

            tagLength = len(tag)

            # ###################################
            #
            # 进入子标签
            #
            # ###################################

            # for i in range(0, len(url)):
            #
            #     print url[i] + ' --------' + unicode(unicode_to_str(tag[i], 'utf-8').strip(), 'utf-8')
            # exit(1)
            for i in range(0, tagLength):
            # for i in range(0, 2):
                tags = {}
                tags['city'] = city
                tags['bigtag'] = unicode(bigtagName, 'utf-8')
                tags['smalltag'] = unicode(unicode_to_str(tag[i], 'utf-8').strip(), 'utf-8')

                urlto = urljoin(rootUrl, url[i])

                yield Request(urlto, headers={'User-Agent': browAgent},
                              meta={'tag':tags}, callback=self.parseTagUrl)




    def parseTagUrl(self, response):

        tags = response.meta['tag']
        shopSel = Selector(response)
        shopSites = shopSel.xpath('//div/ul/li/div[@class="txt"]/div[@class="tit"]')

        titles = shopSites.xpath('a[@data-hippo-type="shop"]/@title').extract()
        urls = shopSites.xpath('a[@data-hippo-type="shop"]/@href').extract()

        listLen = len(titles)

        items = []
        links = []
        for i in range(0, listLen):

            item = ShopDetail()
            item['tag1'] = tags['bigtag']
            item['tag2'] = tags['smalltag']
            item['city'] = tags['city']
            item['name'] = unicode(unicode_to_str(titles[i],'utf-8'), 'utf-8')
            item['link'] = urljoin(rootUrl, urls[i])
            links.append(urljoin(rootUrl, urls[i]))
            items.append(item)

        # del items[2:len(items)]

        itemsLen = len(items)

        for i in range(0, itemsLen):
            yield items[i]
            # yield  Request(links[i], headers={'User-Agent': browAgent},
            #               meta={'item':items[i]}, callback=self.parseShopDetail)

        nextpage = shopSel.xpath('//div[@class="page"]/a[@class="next"]/@href').extract()


        if len(nextpage) != 0:
            url = urljoin(rootUrl, nextpage[0])
            yield Request(url, headers={'User-Agent': browAgent},
                              meta={'tag':tags}, callback=self.parseTagUrl)





    def parseShopDetail(self, response):
        shopDetailSel = Selector(response)
        item = response.meta['item']
        tags = shopDetailSel.xpath('//div[@class="breadcrumb"]/a[@itemprop="url"]/text()').extract()


        name = shopDetailSel.xpath('//h1[@class="shop-name"]/text()').extract()
        address = shopDetailSel.xpath('//div[@itemprop="street-address"]/span[@class="item"]/text()').extract()


        tel = shopDetailSel.xpath('//p[@class="expand-info tel"]/span[@class="item"]/text()').extract()

        lnglat = shopDetailSel.xpath('//div[@id="aside"]/script').extract()
        lnglat = lnglatPa.findall(str(lnglat[0]))
        if len(lnglat) == 0:
            lnglat = '{"lng": 0, "lat": 0}'
        else:
            lnglat = lnglat[0].replace('(', '').replace(')', '')\
                .replace('lng','"lng"').replace('lat','"lat"')


        lngjson = json.loads(lnglat)
        lng = lngjson['lng']
        lat = lngjson['lat']



        #item['name'] = unicode(unicode_to_str(name[0], 'utf-8').strip(), 'utf-8')
        item['address'] = unicode(unicode_to_str(address[0], 'utf-8').strip(), 'utf-8')
        if len(tel) == 0:
            item['tel'] = ''
        else:
            item['tel'] = tel[0]
        item['lng'] = lng
        item['lat'] = lat

        return item






