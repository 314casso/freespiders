# -*- coding: utf-8 -*-
import sys
import os
from os.path import dirname
import logging
import datetime
import xmlrpclib
from spinner.local_settings import SERVERS
import ssl

PROJECT_PATH = dirname(dirname(dirname(os.path.realpath(__file__))))
sys.path.append(PROJECT_PATH)

from spinner.models import SpiderItem
from spinner.settings import SITE_ROOT

logging.basicConfig(filename=os.path.join(SITE_ROOT, 'xmlrpc.log'),level=logging.INFO, format='%(asctime)s %(message)s')

def get_context(srvr):        
    if srvr.get('ssl') == True:    
        context = ssl.create_default_context(cafile=srvr['cafile'])
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(srvr['pemfile'], keyfile=srvr['keyfile'])
        return context

def get_proxy(key='local'):
    srvr = SERVERS[key]
    context = get_context(srvr) 
    proxy = xmlrpclib.ServerProxy(srvr['url'], allow_none=True, context=context)
    return proxy

q = SpiderItem.select().where(SpiderItem.status==SpiderItem.NEW) 
for item in q:
    item_dict = item.get_item_dict()        
    proxy = get_proxy('prime')
    try:
        result = proxy.add_lot(item_dict)
        status = result.get('status')        
        if status == SpiderItem.PROCESSED:
            item.estate_id = result['estate_id']
            item.status = SpiderItem.PROCESSED    
            logging.info("Processed estate_id: %s" % item.estate_id)                    
        elif status is not None:
            item.status = status
            logging.error(result['error_message'])        
        else:
            logging.error('Result without status')
        item.event_date = datetime.datetime.now()
        item.save()
    except Exception, e:
        logging.error(str(e)) 
        


    