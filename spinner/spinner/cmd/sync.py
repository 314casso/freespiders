# -*- coding: utf-8 -*-
import sys
import os
from os.path import dirname
import logging
import datetime
import xmlrpclib
import ssl
import socket

PROJECT_PATH = dirname(dirname(dirname(os.path.realpath(__file__))))
sys.path.append(PROJECT_PATH)

from spinner.utils.utils import Indicator
from spinner.models import SpiderItem
from spinner.settings import SITE_ROOT
from spinner.local_settings import SERVERS

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
lots = len(q)
ind = Indicator(lots)

remote_settings_key = 'local' if socket.gethostname() == 'picasso-kubuntu' else 'prime'

for item in q:        
    item_dict = item.get_item_dict()              
    proxy = get_proxy(remote_settings_key)    
    try:
        ind.update()
        result = proxy.add_lot(item_dict)
        status = result.get('status')        
        if status == SpiderItem.PROCESSED:
            item.estate_id = result['estate_id']
            item.status = SpiderItem.PROCESSED    
            logging.info("id: %s, processed estate_id: %s" % (item.id, item.estate_id))                    
        elif status is not None:
            item.status = status
            logging.error("id: %s, %s" % (item.id, result['error_message']))        
        else:
            logging.error('id: %s, result without status' % item.id)
        item.event_date = datetime.datetime.now()
        item.save()
    except Exception, e:
        logging.error(str(e)) 
        


    