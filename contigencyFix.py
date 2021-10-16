from bs4 import BeautifulSoup as bs
import re
from PIL import Image
import requests
import json
import imageedit

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import fetch
import generator

import os
with open('./json/charlist.json') as f:
    data=json.load(f)

chardata={}
for char in data:
    charname=char["char_name"]
    with open('./json/'+charname+'.json')as f:
        chardata=json.load(f)
    print(charname)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://alchemystars.kloenlansfiel.com/aurorian/"+charname)
    soup=bs(driver.page_source,'html.parser')
    driver.close()
    # with open("../web_download/kloansfiel.html") as f:
    #     target=f.read()

    # soup=bs(target,'html.parser')
    tabs=soup.find('ul',{'class':'aurorian-tabs uk-switcher'})
    tabs=tabs.find_all('li',recursive=False)
    # tab 0 => stat skip completed already
    # tab 1 => skill 
    profile=tabs[5]
    #description
    spanned_profile=profile.find_all('p')
    chardata['description']=spanned_profile[0].getText()
    for i in range(1,len(spanned_profile)):
        tmp=spanned_profile[i].getText().split(': ')
        #realName
        if(tmp[0]=='Name'):
            chardata['realName']=tmp[1]
        #nickname
        if(tmp[0]=='Nickname'):
            chardata['nickname']=tmp[1]
        #gender
        if(tmp[0]=='Gender'):
            chardata['gender']=tmp[1]
        #height
        if(tmp[0]=='Height'):
            chardata['height']=tmp[1]
        #birthday
        if(tmp[0]=='Birthday'):
            chardata['birthday']=tmp[1]
        #birthplace
        if(tmp[0]=='Birthplace'):
            chardata['birthplace']=tmp[1]
        #fighting style
        if(tmp[0]=='Fighting Style'):
            chardata['style']=tmp[1]
    with open('./json/{charname}.json'.format(charname=charname),'w') as x:
        json.dump(chardata, x, indent = 1)