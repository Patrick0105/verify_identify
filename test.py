import base64
import ddddocr
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


ocr = ddddocr.DdddOcr()
a = 0
def OpenBrowser():
    mainUrl = "https://gen.caca01.com/ttcode/codeking"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    global browser
    browser = webdriver.Chrome('/Users/patrick/Desktop/test/chromedriver')
    browser.get(mainUrl)
    browser.maximize_window()
    browser.execute_script('window.scrollTo(0, 500)')

def StartInit():
    while 1:
        try:
            browser.find_element(By.XPATH,"//button[@id='start']").click()
            time.sleep(3)
            break
        except:
            print ('Init Error')
def GetImage():
        while 1:
            global a
            try:
                global img_base64
                img_base64 = browser.execute_script("""
        var ele = arguments[0];
        var cnv = document.createElement('canvas');
        cnv.width = ele.width; cnv.height = ele.height;
        cnv.getContext('2d').drawImage(ele, 0, 0);
        return cnv.toDataURL('image/jpeg').substring(22);    
        """, browser.find_element(By.XPATH,"//img[@id='yw0']"))

                with open("captcha_login.png", 'wb') as image:
                    image.write(base64.b64decode(img_base64))
                with open('captcha_login.png', 'rb') as f:
                    img_bytes = f.read()
                    global res
                res = ocr.classification(img_bytes)
                browser.find_element(By.XPATH,"//input[@id='code']").send_keys(res)
                browser.find_element(By.XPATH,"//input[@id='code']").send_keys('\ue007')
                
            except:
                if a <= 30:
                    a += 1
                    print(f'Wait for next Image...{a}')
                else:
                    print('Ended')
                    break
        
if __name__ =='__main__':
    OpenBrowser()
    StartInit()
    GetImage()
