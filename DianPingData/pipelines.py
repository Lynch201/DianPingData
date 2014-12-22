# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class DianpingdataPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '127.0.0.1',
            db = 'wifi',
            user = 'root',
            passwd = '123456',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )

    def process_item(self, item, spider):
        # query = self.dbpool.runInteraction(self._conditional_insert, item)
        # print '--------' + str(item)
        return item




    def _conditional_insert(self, tx, item):

        tx.execute('insert into shop values (%s, %s, %s, %s, %s, %s, %s, %s)',
                       (item['name'], item['city'], item['tel'], item['tag1'], item['tag2'], item['addredd'],
                        item['lng'],item['lat'],))