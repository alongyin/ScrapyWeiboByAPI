# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#-*- coding=utf-8 -*-
from scrapy import log
from twisted.enterprise import adbapi
import time
import MySQLdb.cursors

class ScrapyweibobyapiPipeline(object):

    def __init__(self):
        # @@@ hardcoded db settings
        # TODO: make settings configurable through settings
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                host='192.168.1.153',
                db='weibodata',
                user='spider',
                passwd='spider1234',
                cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8',
                use_unicode=True
            )

    def process_item(self, item, spider):
        
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread

        if item["tid"] == 3:
            tx.execute(\
                "insert into user_table (uid, sname, location,create_at,verified,follower_count,friend_count,tid,eid)"
                "values (%s, %s, %s,%s, %s, %s,%s,%s, %s)",
                (    item['uid'],
                     item['sname'],
                     item['location'],
                     item['created_at'],
                     item['verified'],
                     item['followers_count'],
                     item['friends_count'],
                     item['tid'],
                     item['eid'],
                 )
            )
        else :
            tx.execute(\
                "insert into event_data (mid, uid, cnt,pos, time, tid, eid)"
                "values (%s, %s, %s, %s, %s, %s, %s)",
                (    item['mid'],
                     item['uid'],
                     item['content'],
                     item['pos'],
                     item['time'],
                     item['tid'],
                     item['eid']
                 )
            )

        log.msg("Item stored in db: %s" % item["uid"], level=log.INFO)
    def handle_error(self, e):
        log.err(e)
