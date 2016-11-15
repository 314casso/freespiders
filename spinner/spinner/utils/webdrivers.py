from selenium import webdriver
import base64
import md5
import os
import datetime
import subprocess
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from spinner.settings import MEDIA_ROOT
from spinner.settings import AVITO_LOGIN


class AvitoWebdriver(object):       
    _driver = None 
    name = 'avito_webdriver'        
    def __init__(self, do_login=True):               
        self.IMAGE_ROOT = os.path.join(MEDIA_ROOT, 'spyder', 'avito')        
        self._do_login = do_login 
                
    def get_driver(self):
        if not self._driver:        
            driver = self._get_driver()
            if self._do_login and driver:
                self.login_avito(driver)
            self._driver = driver    
        return self._driver
    
    def _get_driver(self):   
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            "(KHTML, like Gecko) Chrome/15.0.87"
        )
        return webdriver.PhantomJS(port=65000, desired_capabilities=dcap)

    def login_avito(self, driver):     
        AVITO_LOGIN   
        username = AVITO_LOGIN['username']
        password = AVITO_LOGIN['password']
        login_url = AVITO_LOGIN['login_url']    
        driver.get(login_url)  
        try:
            WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_name("password")).send_keys(password)
        except WebDriverException:
            return # already loged in                     
        WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_name("login")).send_keys(username)        
        WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_class_name("button-origin-yellow")).submit()        
    
    def get_full_filename(self, url):   
        today = datetime.date.today()
        directory = os.path.join(self.IMAGE_ROOT, today.strftime('%m%Y'))
        if not os.path.exists(directory):
            os.makedirs(directory)        
        filename = '%s.png' % md5.new(url).hexdigest()
        full_filename = os.path.join(directory, filename)
        if os.path.isfile(full_filename):
            return full_filename
           
        driver = self.get_driver()                                
        driver.get(url)           
        elem = driver.find_element_by_class_name("js-item-phone-button_card")
        elem.click()        
        WebDriverWait(driver, 10).until(lambda driver : driver.find_elements(By.XPATH, '//div/div/button/img'))           
        res = driver.execute_script("""
          var imgs = document.evaluate("//div/div/button/img", document, null, XPathResult.ANY_TYPE, null);
          var phone_img = imgs.iterateNext();
          var canvas = document.createElement("canvas");
          canvas.width = 315;
          canvas.height = 50;
          var ctx = canvas.getContext("2d");          
          ctx.drawImage(phone_img, 0, 0);
          return canvas.toDataURL("image/png").split(",")[1];
        """)       
        plaindata = base64.b64decode(res)        
        f = open(full_filename, "wb")
        f.write(plaindata)    
        f.close() 
        subprocess.call('convert %s -transparent "#FFFFFF" -alpha background %s' % (full_filename, full_filename), shell=True)
        return full_filename        
