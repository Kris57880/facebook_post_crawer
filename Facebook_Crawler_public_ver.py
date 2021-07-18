
from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from msedge.selenium_tools import EdgeOptions
from bs4 import BeautifulSoup as Soup
import os
import time 
import requests

#use pip to install the import files 

options = EdgeOptions()
options.use_chromium = True
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)

keyword = ['贈',"送","免費","$0","free","FREE"] #你想要的關鍵字
taboo = ["送到","送去","送的","贈品","外送"] #假關鍵字

id = "your facebook id "
pwd = "your facebook passward "
driver = webdriver.Chrome(executable_path="C:\edgedriver_win64/MicrosoftWebDriver.exe", options=options)
url = "https://facebook.com"
specurl = "https://www.facebook.com/groups/817620721658179" #你想爬的社團
history_post = []

def scroll(scrolltimes):
  for i in range(scrolltimes):
    js = 'window.scrollTo(0,document.body.scrollHeight/2 );'
    driver.execute_script(js)
    time.sleep(2)

def line_message(msg):
    token = "your line token" #see https://xenby.com/b/274-%E6%95%99%E5%AD%B8-%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8-line-notify-%E5%B0%8D%E7%BE%A4%E7%B5%84%E9%80%B2%E8%A1%8C%E9%80%9A%E7%9F%A5
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
   }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

def check_keyword(post):
    flag = False 
    for j in keyword : 
        if j in post :
            for i in taboo:
                if i  in post :
                    flag= True 
            if flag is False:     
                line_message("青椒二手拍上有贈送活動!!!\n"+post+'\n'+'https://www.facebook.com/groups/817620721658179')

driver.get(url)
email = driver.find_element_by_id("email")
email.send_keys(id)

passward = driver.find_element_by_id("pass")
passward.send_keys(pwd)

bottom = driver.find_element_by_name("login")
bottom.click()
time.sleep(3)


#span = driver.find_element_by_class_name("rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.i1fnvgqd.bp9cbjyn.owycx6da.btwxx1t3.jeutjz8y")
#span.click()

while True:
    driver.get(specurl)
    time.sleep(1)
    #scroll(1)   
    bottom = driver.find_elements_by_class_name("oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.oo9gr5id.gpro0wi8.lrazzd5p")
    if len(bottom)>1 and "查看更多"in bottom[1].text:
        bottom[1].click()  
    time.sleep(1)
    soup = Soup(driver.page_source, "html.parser")
    post = soup.find(class_='ecm0bbzt hv4rvrfc e5nlhep0 dati1w0a')

    Time = ''
    Timeframe = soup.find(class_= 'b6zbclly myohyog2 l9j0dhe7 aenfhxwr l94mrbxd ihxqhq3m nc684nl6 t5a262vz sdhka5h4')
    if Timeframe is not None:
        Time = Timeframe.text
        Time.strip('=')

    if post is None:
        post = soup.find(class_='ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a')
            
    if post is not None and post.text not in history_post and  "剛剛"  in Time:
        history_post.append(post.text)
        print('history-------')
        print(history_post,'\n')
        print('--------------------------\n\n')
        print('new Post !!')
        print(post.text)
        check_keyword(post.text)

os.system("pause")