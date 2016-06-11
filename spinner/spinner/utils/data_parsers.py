# -*- coding: utf-8 -*-
import re
from spinner.utils.utils import join_strings

def abstractmethod(method):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method)) 
    default_abstract_method.__name__ = method.__name__     
    return default_abstract_method

class BaseFieldsParser(object):
    _phone = None
    _title = None
    _prices = None
    _locality = 0   
    def __init__(self, sel, url, meta=None):                     
        self._sel = sel  
        self._url = url
        self._meta = meta 
    
    @abstractmethod
    def title_parser(self): pass     
    
    @abstractmethod
    def estate_type_parser(self): pass
    
    @abstractmethod
    def phone_parser(self): pass        
    
    @abstractmethod
    def room_count_parser(self): pass
        
    @abstractmethod    
    def region_parser(self): pass
    
    @abstractmethod
    def locality_parser(self): pass
    
    @abstractmethod
    def name_parser(self): pass
    
    @abstractmethod
    def desc_parser(self): pass
    
    @abstractmethod
    def price_parser(self): pass
    
    @abstractmethod
    def mesure_parser(self): pass
    
    def phone(self):
        return self.filter_phone()
    
    def name(self):
        return self.name_parser()
    
    def description(self):
        return self.desc_parser()
    
    def prices(self):
        if not self._prices:            
            price = join_strings(self.price_parser())
            mesure = join_strings(self.mesure_parser())             
            price_str = ['%s %s' % (price, mesure) if price else '']
            price_digit = [self.digit_price(price, mesure)]
            self._prices = {'price' : price_str, 'price_digit' : price_digit}
        return self._prices
    
    def url(self):
        return [self._url]
    
    def estate_type(self):
        return self.estate_type_parser()  
        
    def locality(self):
        if not self._locality:
            self._locality = self.get_locality() 
        return self._locality
    
    def room_count(self):
        room_parser_result = self.room_count_parser()
        if room_parser_result:
            result = join_strings(room_parser_result)
            return re.sub('\D','', result)
    
    def populate_item(self, item):        
        item['phone'] = self.phone()         
        item['name'] = self.name()
        item['note'] = self.description()                    
        item['price'] = self.prices()['price']
        item['price_digit'] = self.prices()['price_digit']
        item['url'] = self.url()
        item['estate_type_id'] = self.estate_type()                        
        item['locality_id'] = self.locality()        
        item['room_count'] = self.room_count()  
    
    def title(self):
        if not self._title:
            self._title = join_strings(self.title_parser())
        return self._title
    
    def re_mapper(self, mapper, txt):
        if txt:
            for key, value in mapper.iteritems():
                matches = re.search(key, txt, re.I | re.U)            
                if matches:
                    return value 
    
    def price_mesures(self):
        return {u'т.р.':1000, u'млн.р.':1000000, u'тыс. руб.':1000, u'руб.': 1}
            
    def digit_price(self, price, mesure):
        mesures = self.price_mesures()
        if price:
            if mesure in mesures:
                price_digit = float(re.sub('\D','', price))
                price_digit = int(price_digit * mesures[mesure])                
                return price_digit
        return 0
    
    def filter_phone(self):
        phone = self.phone_parser()
        if not phone:
            return            
        phone_str = join_strings(phone,',')
        phones = re.split(r'[\,|\n]', phone_str)
        result = []
        for phone in phones:         
            phone = phone.strip().replace('+7', '8')
            result.append(re.sub('\D','', phone))
        return result
            
    def get_locality(self, field_name='name'):
        return self.locality_parser() 
            
class BasePhoneImageParser(BaseFieldsParser):
    def populate_item(self, item):
        super(BasePhoneImageParser, self).populate_item(item)
        item['phone_filename'] = self.phone_filename()
        item['phone_guess'] = self.phone_guess()
    
    @abstractmethod
    def phone_filename(self):
        pass
    
    @abstractmethod
    def phone_guess(self):
        pass
