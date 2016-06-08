# -*- coding: utf-8 -*-
from urlparse import urlparse
from spinner.models import SpiderItem

def join_strings(strings, delim=u''):
    if not strings:
        return None
    result = [x.strip() for x in strings if x.strip()]
    return delim.join(result)

def process_value_base(value, spider_name):
    print "processing... %s for spider %s" % (value, spider_name)              
    q = SpiderItem.select().where(SpiderItem.url==value, SpiderItem.spider==spider_name, SpiderItem.status!=SpiderItem.ERROR) 
    if q:
        print '%s skiping...' % value
        return None    
    return value

def get_url_path(url):        
    if url:
        link = url if isinstance(url, basestring) else url[0]                 
        o = urlparse(link)
        return o.path
