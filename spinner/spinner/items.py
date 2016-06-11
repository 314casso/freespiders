# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class AvitoItem(Item):            
    phone = Field()    
    note = Field()
    name = Field()
    price = Field()
    price_digit = Field()
    url = Field()
    estate_type_id = Field()
    locality_id = Field()   
    estate_number = Field()
    room_count = Field()   
    phone_filename = Field()
    phone_guess = Field()
        
    def print_item(self):
        try:        
            print u'********* ITEM *********'
            for key, value in self._values.iteritems():
                txt = u''
                if type(value) is list:
                    for v in value:
                        txt += u'%s ' % v                                     
                else:
                    txt = u'%s' % value            
                print u"KEY [ %s: %s ]" % (key, txt)
            print u'********* END *********'
        except:
            print u'PRINT ITEM ERROR'  
