import scrapy
import json
from netease.items import NeteaseItem 
import re
class NewsSpider(scrapy.Spider):
    name = 'tech163'
    step_base = 20
    page_base = 10
    url_offset_range = range(0,page_base*step_base, step_base)
    detail_url = 'http://j.news.163.com/%s'
    comment_url = 'http://comment.news.163.com/cache/newlist/comment_bbs/%s_1.html'
    content_url = 'http://j.news.163.com/hy/doc.s?docid=%s'
    base_url = 'http://j.news.163.com/hy/newshot.s?channel=7&limit=%s&offset=%s'
    start_urls = [ base_url % (step_base, x) for x in url_offset_range ]

    def parse(self, response):
        #获得
        data = json.loads(response.body)
        self.log( 'data[%s] len[%s]' % (response.url,len(data)) )

        for listitem in data:

            req = scrapy.Request( self.content_url % listitem['docID'], self.fetchDetail)
            req.meta['listjson'] = listitem
            req.meta['docID'] = listitem['docID']
            item = NeteaseItem()

            #item['origin_url']  = listitem['url_163']
            item['title']       = listitem['title']
            item['category']    = listitem['category'].split('/')[0]
            if 'source' in listitem:
                item['author']      = listitem['source']
            if 'tcount' in listitem:
                item['read_count']  = listitem['tcount']

            if 'pic_url' in listitem:
                listitem['pic_url'] = json.loads(listitem['pic_url'])
                item['cover_url'] = len(listitem['pic_url']) and listitem['pic_url'][0]['url']

            req.meta['item'] = item
            yield req



    def fetchDetail(self, response):
        data = json.loads(response.body)
        response.meta['item']['content'] = data['content']

        yield response.meta['item']
        #req = scrapy.Request( self.comment_url % response.meta['docID'], self.fetchComment, errback=self.fetchCommentFail)
        #req.meta['item'] = response.meta['item']

        #yield req

    def fetchCommentFail(self, fail):
        return fail

    def fetchComment(self, response):

        data = ''
        try:
            data = response.body
        
            reBegin = re.compile(r'^[^{]+')
            reEnd = re.compile(r'[^}]+$')
            data = reBegin.sub('', data)
            data = reEnd.sub('', data)
            data = json.loads(data)
        except:
            data = None

        response.meta['item']['comment'] = data and data['newPosts']

        yield response.meta['item']

