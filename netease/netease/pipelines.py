# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class NeteasePipeline(object):
    def __init__(self):
        self.file = open(u'items.json', u'wb')
        self.fileSql = open(u'items.sql', u'wb')

    def process_item(self, item, spider):
        
        data = dict(item)
        
        if "ph.126.net" in data['cover_url'] or len(data['cover_url'])==0:
          return item

        line = json.dumps(data) + ",\n"
        self.file.write(line)

        print '============='
        print data.keys()

        sqlCategory = u"insert into tbl_category (name) values ('{category}');".format(**data)
        sqlAuthor = u"insert into tbl_user (username, passwd, nickname, salt) values ('system_{author}', 'nologin','{author}', 'nologin');".format(**data)
        sqlNews = u"insert into tbl_news (title, category_id, content, author_id, cover_url) values ('{title}', (select id from tbl_category where name='{category}'),'{content}', (select id from tbl_user where username='system_{author}'), '{cover_url}');".format(**data)
        sqlNewsUpdate = u"update tbl_news set content='{content}', cover_url='{cover_url}', read_count={read_count} where title='{title}';".format(**data) 
        line = sqlCategory +u"\n" + sqlAuthor + u"\n" + sqlNews + u"\n" + sqlNewsUpdate+ "\n"
        self.fileSql.write(line)

        
        return item