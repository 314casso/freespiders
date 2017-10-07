# -*- coding: utf-8 -*-
from spinner.utils.data_parsers import BasePhoneImageParser
from spinner.utils.vector import ImageDecoder, VectorCompare
from spinner.utils.utils import  join_strings
import re
from urlparse import urlparse
from spinner.data.external_mappers import EstateTypeMapper
import os
from spinner.settings import MEDIA_ROOT
from spinner.pipelines import avito_webdriver

DECODER_SETTINGS = {
           'avito_phone': {
                            'icons_path': os.path.join(MEDIA_ROOT, 'avito_lib'),
                            'iconset': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                            }                     
           }

class AvitoFleldsParser(BasePhoneImageParser): 
    _phone_data = None  
    _breadcrumb = None   
      
    def __init__(self, *a, **kw):
        self.data = kw.pop('data')
        self.localities = self.data['localities']        
        super(AvitoFleldsParser, self).__init__(*a, **kw)
        
    def title_parser(self):
        return set(self._sel.xpath('//h1[contains(@class, "title-info-title")]/span/text()').extract())

    def breadcrumbs_parser(self):
        breadcrumbs = self._sel.xpath('//a[contains(@class, "breadcrumb-link")]/text()')
        
        breadcrumb = breadcrumbs[-1].extract().lower()
        return breadcrumb

    def get_breadcrumbs(self):
        if not self._breadcrumb:            
            self._breadcrumb = self.breadcrumbs_parser()
        return self._breadcrumb
                 
    def estate_type_parser(self):
        mapper = {
                  
                         ur'вторичка' : EstateTypeMapper.KVARTIRA,
                         ur'cтудии' : EstateTypeMapper.KVARTIRASTUDIYA,
                         ur'новостройки' : EstateTypeMapper.NOVOSTROYKA,
                         ur'комнаты' : EstateTypeMapper.KOMNATA,
                         ur'дачи' : EstateTypeMapper.DACHA,
                         ur'дома' : EstateTypeMapper.DOM,
                         ur'коттеджи' : EstateTypeMapper.KOTTEDZH,
                         ur'таунхаусы': EstateTypeMapper.TAUNHAUS,
                         ur'поселений': EstateTypeMapper.UCHASTOKDLYASTROITELSTVADOMA,
                         ur'сельхозназначения': EstateTypeMapper.UCHASTOKSELSKOHOZYAYSTVENNOGONAZNACHENIYA,
                         ur'промназначения': EstateTypeMapper.UCHASTOKINOGONAZNACHENIYA,
                         ur'гостиница' : EstateTypeMapper.GOSTINITSA,
                         ur'офисное' : EstateTypeMapper.OFIS,
                         ur'свободного' : EstateTypeMapper.ZDANIE,
                         ur'производственное' : EstateTypeMapper.PROIZVODSTVENNAYABAZA,
                         ur'складское' : EstateTypeMapper.SKLAD,
                         ur'торговое' : EstateTypeMapper.MAGAZIN,
                         } 
        txt = self.get_breadcrumbs()                
        if txt:           
            result = self.re_mapper(mapper, txt)
            if callable(result):
                return result()
        return result or EstateTypeMapper.ZDANIE
        
    def phone_parser(self): 
        return self._sel.xpath('//i[contains(@class, "icon-phone-sign")]/../text()').extract()        
    
    def room_count_parser(self):
        title = self.title()
        m = re.search(ur'(?P<room_cnt>\d)\-к', title, re.I | re.U)
        if m:
            return m.group('room_cnt')  
    
    def locality_parser(self):
        parse_object = urlparse(self._url)
        parts = parse_object.path.split('/')           
        for part in parts:
            l = self.localities.get(part)
            if l:
                return l 
    
    def name_parser(self):
        return set(self._sel.xpath('//div[contains(@class, "item-view-seller-info")]//div[contains(@class, "seller-info-name")]/a/text()').extract())  
    
    def desc_parser(self):        
        result = []
        result.append(self.title())
        result.append('\n')
        result.append(join_strings(set(self._sel.xpath('//div[@itemprop="description"]//text()').extract()), ', '))        
        return result
    
    def price_parser(self):
        return self._sel.xpath('//div[contains(@class, "item-view-right")]//span[contains(@class, "price-value-string")]/text()').re(r'\d')
    
    def mesure_parser(self):
        return u'руб.'
    
    def locality_id(self):
        if not self._locality_id:
            self._locality_id = self.locality_parser()            
        return self._locality_id
    
    def get_phone_data(self):
        if not self._phone_data:            
            self._phone_data = self.decode_phone(self._url)            
        return self._phone_data
    
    def phone(self):        
        return [self.get_phone_data()['phone']]
    
    def phone_filename(self):      
        return self.get_phone_data()['filename']
    
    def phone_guess(self):      
        return self.get_phone_data()['guess']
    
    def decode_phone(self, url):
        print "decode %s" % url
        full_filename = avito_webdriver.get_full_filename(url)
        print "full_filename %s" % full_filename
        if not full_filename:
            return {'filename': None, 'guess': 0, 'phone': None}
        image_decoder = ImageDecoder(DECODER_SETTINGS['avito_phone'], VectorCompare())
        result = image_decoder.decode(full_filename)
        guess = result[1]
        phone = ''.join(result[0])        
        return {'filename': full_filename, 'guess': guess, 'phone': phone} 
  
   
