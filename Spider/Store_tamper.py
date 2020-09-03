from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import requests, os, sys, time, threading, socket, mysql.connector , subprocess
from datetime import datetime
from lxml import html

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local = socket.gethostname()
port = 8080
   

_sql = mysql.connector.connect(
    host='localhost',user='root',password='',database='Raporter'
)

class Screenshot:
    def __init__(self,category,url):
        self.link = url
        self.category = category
        self.id = str(int(round(time.time() * 1000)))
    def config_browser(self):
        option = Options()
        option.headless = True
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-extensions')
        option.add_argument('--disable-gpu')
        option.add_argument('--log-level=3')
        #option.add_argument('--user-data-dir=Selenium')
        option.add_argument('--no-sandbox')
        return option
    
    def take(self):
        chrome.get(self.link)
        self.Click('button[data-role="close-and-accept-consent"]')
        img_name = '../content/Offers/{}_{}.png'.format(self.category,self.id)
        chrome.save_screenshot(img_name)
        return img_name

    
    '''
    #Check if target element exists
    '''
    def Exists(self,element):
        try:
            chrome.find_element_by_css_selector(element)
            return True
        except NoSuchElementException:
            return False
    
    '''
    #Click on the certain elements
    '''
    def Click(self,target):
        if self.Exists(target):
            chrome.find_element_by_css_selector(target).send_keys(Keys.RETURN)
        else:
            return ""



class Network:
    def __init__(self):
        self.gate = 'http://192.168.1.222/raporter/index.php?'
    
    def agent(self):
        _uagent = self.post(self.gate, {'random':''})
        return {'User-Agent':_uagent}

    def write_store(self,name,category):
        return self.post(self.gate,{'write_store':name,'category':category})
    
    def write_page(self,category,link):
        return self.post(self.gate, {
                'write_page':'','category':category, 'link':link
            })

    def get(self, url):
        try:
            time.sleep(.5)
            return requests.get(url, headers = self.agent()).content.decode('utf-8')
        except Exception as ex:
            Debug(0,'ERROR',str(ex))
            time.sleep(.5)
            return requests.get(url, headers = self.agent()).content.decode('utf-8')
       

    def post(self,url,data):
        return requests.post(url, data=data).text
    
    def Connect(self):
        if screen:
            sock.connect((local,port))

    def Send(self,data):
        if sock is not None:
            sock.send(data.encode())
            


class Categories:
    def __init__(self,url):
         self.map = url
         self.xpath = '''//a[@class="_w7z6o"][contains(@href,'/kategoria/')]/@href'''
    
    def Load_categories(self):
        page = Network().get(self.map)
        tree = html.fromstring(page)
        _categories = tree.xpath(self.xpath)
        for _category in _categories:
            _category = 'https://allegro.pl'+_category
            Paginator(_category.split('/')[4], _category).Add_pages()
        

class Paginator:
    def __init__(self,cat_name,url):
        self.url = url
        self.cat_name = cat_name
        self.xpath = '''substring(//div[@role="navigation"], string-length(//div[@role="navigation"])-2)'''
    
    def Add_pages(self):
        '''
        #Load categories and subcategories
        #and then send to the mysql
        '''
        page = Network().get(self.url)
        tree = html.fromstring(page)
        number = tree.xpath(self.xpath)
        if 'z' in number:
            number = number.replace('z','')
        number = int(number)
        for i in range(number+1):
            link = '{}?p={}'.format(self.url,str(i))
            Debug(1,'Category',self.cat_name)
            Debug(1,'Link', link)
            #Debug(1,'NETWORK',Network().write_page(self.cat_name, link))

class Offers:
    def __init__(self):
        self.link_path = '''//a[contains(@href,'oferta')]/@href'''
        self.store_name = '''//a[@href="#aboutSeller"]/text()'''
        self.category = ''
    
    def LoadPages(self):
        '''
        #Load categories and subcategories
        #from the mysql    
        '''
        if _sql is not None:
            cursor = _sql.cursor()
            cursor.execute('SELECT PAGE_CATEGORY, PAGE_LINK FROM PAGES')
            stack = cursor.fetchall()
            for item in stack:
                self.GetOffer(item[0],item[1])
                
            
    def GetOffer(self,category,link):        
        '''
        #List all offers
        #from the current category
        #and send for store data extraction
        '''
        self.category =category
        Page = Network().get(link)
        tree = html.fromstring(Page)
        links= tree.xpath(self.link_path)
        for link in links:
           self.getStore(link)
            
        
    def getStore(self,link):
        '''
        # Get store name and 
        # actual category 
        '''
        Page = Network().get(link)
        tree = html.fromstring(Page)
        name= tree.xpath(self.store_name)[0]
        
        resp = Network().write_store(name,self.category) 
        print(resp)
        if screen and  resp != 'duplicate':
            Debug(1,'[OFFER]', link)
            self.Visualize(link,name,self.category)

    def Visualize(self,link,store,category):
        img = Screenshot(category,link).take()
        Network().Send('stack_{}${}${}${}'.format(
            link,store,category,img
        ))
                    


class Analyzer:
    def Run(self):
        Network().Connect()
        time.sleep(1)
        Offers().LoadPages()

    def noScreen(self):
        Offers().LoadPages()

def Debug(status,arg,data):
    Now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status is not None and arg != "" and data !="":
        if status > 0:
            print('['+str(Now)+'] [+] ' + data + '\n')
        else:
            print('['+str(Now)+'] [-] ' + data + '\n')

chrome = webdriver.Chrome(executable_path=r"/usr/lib/chromium-browser/chromedriver", chrome_options=Screenshot('','').config_browser())
screen = None
if __name__ == '__main__':
    try:
        #Categories('https://allegro.pl/mapa-strony/kategorie').Load_categories()
        
        if sys.argv[1] is not None and sys.argv[2] is not None:
            cmd_1 = sys.argv[1]
            cmd_2 = sys.argv[2]
            if cmd_1 == "analysis" and cmd_2 == 'screenshot':
                screen = True
                Analyzer().Run()
            if cmd_1 == "analysis" and cmd_2 == 'noscreen':
                Analyzer().noScreen()
                screen = False
                
    except KeyboardInterrupt:
        chrome.quit()
        Debug(0,'INFO','TERMINATED BY USER')
    except IndexError:
        Debug(0,'ERROR', 'EMPTY COMMAND')