# -*- coding: utf-8 -*-

# Scrapy settings for DianPingData project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'DianPingData'

SPIDER_MODULES = ['DianPingData.spiders']
NEWSPIDER_MODULE = 'DianPingData.spiders'

DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'DianPingData.spiders.rotate_useragent.RotateUserAgentMiddleware' :400,
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
        'DianPingData.middlewares.ProxyGoAgent': 100,
    }
ITEM_PIPELINES = ['DianPingData.pipelines.DianpingdataPipeline']

COOKIES_ENABLES=False
# DOWNLOAD_DELAY = 2
# RANDOMIZE_DOWNLOAD_DELAY = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94
# Safari/537.36'

