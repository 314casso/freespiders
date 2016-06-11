# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spinner.models import SpiderItem
from spinner.utils.utils import get_url_path
from spinner.utils.webdrivers import AvitoWebdriver

avito_webdriver = AvitoWebdriver()

class AvitoPipeline(object): 
    def process_item(self, item, spider):       
        self._create_spyder_meta(spider, item)
        return item
    
    def _create_spyder_meta(self, spider, item):      
        url = self.prepare_value('url', item)          
        spider_item, created = SpiderItem.create_or_get(spider=spider.name, url=url)  # @UnusedVariable
        for key in item.iterkeys():
            value = self.prepare_value(key, item)
            if value:
                setattr(spider_item, key, value)        
        spider_item.set_status()
        spider_item.origin_id = spider.ORIGIN_ID
        full_url = item['url']
        spider_item.full_url = full_url if isinstance(full_url, basestring) else full_url[0]            
        spider_item.save()
        return spider_item

    def prepare_value(self, key, item):
        if key not in item or not item[key]:
            return None                       
        value = item[key]
        if key == 'url':
            return get_url_path(value)                               
        if type(value) in (int, float, str):
            return value        
        if len(value) == 1:
            return value[0]        
        value = [u'%s' % v for v in value if v]
        return u','.join(value) 
    