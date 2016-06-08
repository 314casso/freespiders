# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from urlparse import parse_qs, urlparse
from scrapy.selector import Selector
import re
from scrapy.http import Request
from spinner.items import AvitoItem    
from spinner.data.external_mappers import LocalityMapper    
from spinner.utils.utils import process_value_base
from spinner.utils.avito_parsers import AvitoFleldsParser

def process_value(value):   
    return process_value_base(value, AvitoSpider.name)

class AvitoSpider(CrawlSpider):
    ORIGIN_ID = 1
    MAX_PAGE = 20 
    _last_page = {}
    name = 'avito'
    allowed_domains = ['avito.ru']
    custom_settings = {'DOWNLOAD_DELAY': 5}
    localities = {
#                     'gelendzhik':LocalityMapper.GELENDZHIK,
#                     'anapa': LocalityMapper.ANAPA,
#                     'novorossiysk':LocalityMapper.NOVOROSSIYSK,
#                     'temryuk':LocalityMapper.TEMRYUK,
#                     'abrau-dyurso': LocalityMapper.ABRAUDYURSO,
#                     'anapskaya': LocalityMapper.ANAPSKAYA,
#                     'arhipo-osipovka': LocalityMapper.ARHIPOOSIPOVKA,
#                     'ahtanizovskaya': LocalityMapper.AHTANIZOVSKAYA,
#                     'verhnebakanskiy': LocalityMapper.VERHNEBAKANSKIY,
#                     'vinogradnyy': LocalityMapper.VINOGRADNYY,
#                     'vityazevo': LocalityMapper.VITYAZEVO,
#                     'vyshesteblievskaya': LocalityMapper.VYSHESTEBLIEVSKAYA,
#                     'gayduk': LocalityMapper.GAYDUK,
                    'glebovka': LocalityMapper.GLEBOVSKOE,
#                     'golubitskaya': LocalityMapper.GOLUBITSKAYA,
#                     'gostagaevskaya': LocalityMapper.GOSTAGAEVSKAYA,
#                     'kurchanskaya': LocalityMapper.KURCHANSKAYA,
#                     'kabardinka': LocalityMapper.KABARDINKA,
#                     'divnomorskoe': LocalityMapper.DIVNOMORSKOE,
#                     'dzhiginka': LocalityMapper.DZHIGINKA,
#                     'myshako': LocalityMapper.MYSHAKO,
#                     'natuhaevskaya': LocalityMapper.NATUHAEVSKAYA,
#                     'raevskaya': LocalityMapper.RAEVSKAYA,
#                     'yurovka': LocalityMapper.YUROVKA,
#                     'tsibanobalka': LocalityMapper.TSYBANOBALKA,
#                     'taman': LocalityMapper.TAMAN,
#                     'supseh': LocalityMapper.SUPSEH,
#                     'krasnodarskiy_kray_strelka': LocalityMapper.STRELKA,
#                     'starotitarovskaya': LocalityMapper.STAROTITAROVSKAYA,
#                     'sennoy': LocalityMapper.SENNOY,
                  }  
    rules = (
        Rule(SgmlLinkExtractor(restrict_xpaths=('//div[@class="pagination__nav clearfix"]/a',)), follow=True, process_request='process_request_filter', callback='process_response_filter'),
        Rule (SgmlLinkExtractor(restrict_xpaths=('//a[@class="description-title-link"]',), process_value=process_value), callback='parse_item'),
    )   
       
    def start_requests(self):
        template = "https://www.avito.ru/%s/%s/prodam?user=1&view=list"
        com_template = "https://www.avito.ru/%s/kommercheskaya_nedvizhimost/prodam/%s/za_vse?user=1&view=list"
        urls = []
        
        types = ['kvartiry', 'komnaty', 'doma_dachi_kottedzhi', 'zemelnye_uchastki', 'garazhi_i_mashinomesta', ]
        com_types = ['magazin', 'gostinicy', 'drugoe', 'proizvodstvo', 'sklad', 'ofis']
        for l in self.localities.iterkeys():            
            for t in types:
                urls.append(template % (l, t))                
            for com_type in com_types:
                urls.append(com_template % (l, com_type)) 
        for url in urls:            
            yield Request(url, self.parse)
    
    def parse_item(self, response):
        item = AvitoItem()
        fields_parser = AvitoFleldsParser(Selector(response), url=response.url, data={'localities': self.localities})
        fields_parser.populate_item(item)        
        item.print_item()
        return item

    def process_response_filter(self, response):
        print response.url
        dates = Selector(response).xpath('//span[@class="date"]/text()')
        for date in dates:
            txt = date.extract()
            key = ur'вчера|сегодня'
            matches = re.search(key, txt, re.I | re.U)
            if not matches:
                page_num = self.get_page_num(response.url)
                if page_num:
                    self.set_last_page(response.url, int(page_num))                               
        return []        
    
    def set_last_page(self, url, value):
        path = urlparse(url).path
        self._last_page[path] = value
        
    def get_last_page(self, url):
        path = urlparse(url).path
        return self._last_page.get(path, self.MAX_PAGE) 

    def get_page_num(self, url):        
            qs = parse_qs(urlparse(url).query)
            if 'p' in qs:
                return int(qs['p'][0])
            return 0
        
    def process_request_filter(self, request):              
        if self.get_page_num(request.url) > self.get_last_page(request.url):            
            return None
        return request  
  

      
                                  
