# -*- coding: utf-8 -*-
from peewee import *  # @UnusedWildImport
import datetime
from spinner.settings import SITE_ROOT
import os
from decimal import Decimal

db = SqliteDatabase(os.path.join(SITE_ROOT, 'db', 'spidermeta.db'))

class SpiderItem(Model):
    NEW = 0
    PROCESSED = 1    
    ERROR = 2
    NOPHONE = 3
    EXISTSPHONE = 4
    DO_NOT_PROCESS = 5
    BADPHONE = 6
    STATUS_CHOICES = (
        (NEW, u'Новый'),
        (PROCESSED, u'Обработанный'),
        (ERROR, u'Ошибка'),
        (NOPHONE, u'Нет телефона'),
        (EXISTSPHONE, u'Телефон в базе'),
        (DO_NOT_PROCESS, u'Не обрабатывать'),        
    )
    created = DateTimeField(index=True, default=datetime.datetime.now)
    spider = CharField(index=True, max_length=100)
    url = CharField(index=True, max_length=255)
    full_url = CharField(index=True, max_length=255, null=True)
    status = IntegerField(choices=STATUS_CHOICES, index=True, default=NEW)    
    event_date = DateTimeField(default=datetime.datetime.now())    
    phone = CharField(index=True, max_length=20, null=True)
    phone_filename = CharField(max_length=250, null=True)
    phone_guess = DecimalField(null=True, max_digits=3, decimal_places=2)
    note = TextField(null=True)
    name = CharField(max_length=250, null=True)
    price = CharField(max_length=250, null=True)
    price_digit = IntegerField(null=True)    
    estate_type_id = IntegerField(null=True)    
    locality_id = IntegerField(null=True)
    estate_id = IntegerField(null=True)
    origin_id = IntegerField(null=True)
    microdistrict = CharField(max_length=150, null=True)
    street = CharField(max_length=150, null=True)
    estate_number = CharField(max_length=50, null=True)
    room_count = IntegerField(null=True)    
    
    def set_status(self):  
        if self.phone_guess != 1:
            return SpiderItem.ERROR                  
        if not self.phone:
            self.status = SpiderItem.NOPHONE                
        items = SpiderItem.select().where(
           SpiderItem.phone==self.phone, 
           SpiderItem.status==SpiderItem.PROCESSED
           )
        if items:
            self.status = SpiderItem.EXISTSPHONE       
    
    def get_item_dict(self):        
        meta = {}.fromkeys(['created', 'spider', 'url', 'full_url', 'status', 'event_date', 'phone_guess', 'price'])
        item = {}.fromkeys(['phone', 'note', 'name', 'price_digit', 'estate_type_id', 'locality_id', 'microdistrict', 'street', 'estate_number', 'estate_id', 'origin_id'])
        bidg = {}.fromkeys(['room_count',])
        lot = {'meta': meta, 'item': item, 'bidg': bidg}
        for fieldset in lot.itervalues():
            for key in fieldset.iterkeys():
                value = getattr(self, key)
                if isinstance(value, Decimal):
                    value = float(value)                     
                fieldset[key] = value
        return lot
 
    class Meta:
        database = db
        indexes = (        
            (('spider', 'url'), True),
        )    
        
db.connect()        
db.create_tables([SpiderItem], True)

#db.truncate_tables([PickledItem], True)