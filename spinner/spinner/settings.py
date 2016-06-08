# Scrapy settings for spinner project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
from local_settings import PRIVATE_AVITO_LOGIN

AVITO_LOGIN = PRIVATE_AVITO_LOGIN

BOT_NAME = 'spinner'

ITEM_PIPELINES = {
    'spinner.pipelines.AvitoPipeline': 300,    
}

SPIDER_MODULES = ['spinner.spiders']
NEWSPIDER_MODULE = 'spinner.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
DOWNLOAD_DELAY = 7
LOG_LEVEL = 'INFO'

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
