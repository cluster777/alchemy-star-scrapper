from bs4 import BeautifulSoup as bs
import re
from PIL import Image
import requests
import json


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import fetch
import generator

import os

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
# chrome_options.add_argument('user-agent={0}'.format(user_agent))
# chrome_options.add_argument('window-size=1920x1080');
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://alchemystars.kloenlansfiel.com/aurorian/Carleen")
with open("../web_download/kloansfiel.html") as f:
    target=f.read()

soup=bs(target,'html.parser')
tabs=soup.find('ul',{'class':'aurorian-tabs uk-switcher'})
tabs=tabs.find_all('li',recursive=False)
# tab 0 => stat skip completed already
# tab 1 => skill 
skill=tabs[1]
# skill name  <h4 class="uk-padding-small uk-margin-remove uk-padding-remove">
print(skill.find('h4',{'class':'uk-padding-small uk-margin-remove uk-padding-remove'}).getText())
# tab 2 => equip
equip=tabs[2]
# equip name
print(equip.find('h3').getText())
# equip description
print(equip.find('p').getText())
# equip image need download
url="https://alchemystars.kloenlansfiel.com"+equip.find('img')['data-src']
print(url)
im = Image.open(requests.get(url, stream=True,timeout=20).raw)
im.save("./equip/"+'carleen'+".png",optimize=True,quality=50)
# tab 3 => collosus
collosus=tabs[3]
collosus_span=collosus.find_all('span')
collosus_h=collosus.find_all('h4')
# skill 1
print(collosus_h[0].getText())
print(collosus_span[0].getText())
# skill 2
print(collosus_h[1].getText())
print(collosus_span[1].getText())
    # conversation if available dynamic?
    # furniture if available dynamic?
# tab 4 => gift
gift=tabs[4]
# find the tag and list it as needed
gift_list=gift.find_all('p')
data=[]
for gf in gift_list:
    if(re.search("given to (.*)\.",gf.getText()).group(1) not in data):
        data.append(re.search("given to (.*)\.",gf.getText()).group(1))
print(data)
# tab 5 => profile
profile=tabs[5]
#description
spanned_profile=profile.find_all('span')
for i in range(len(spanned_profile)):
    #nickname
    if(spanned_profile[i].getText()=='Nickname:'):
        print(spanned_profile[i+1].getText())
    #gender
    if(spanned_profile[i].getText()=='Gender:'):
        print(spanned_profile[i+1].getText())
    #height
    if(spanned_profile[i].getText()=='Height:'):
        print(spanned_profile[i+1].getText())
    #birthday
    if(spanned_profile[i].getText()=='Birthday:'):
        print(spanned_profile[i+1].getText())
    #birthplace
    if(spanned_profile[i].getText()=='Birthplace:'):
        print(spanned_profile[i+1].getText())
    #fighting style
    if(spanned_profile[i].getText()=='Fighting Style:'):
        print(spanned_profile[i+1].getText())
# tab 6 => files
files=tabs[6]
files_p=files.find_all('p')
files_h=files.find_all('h4')
data=[]
for i in range(len(files_p)):
    data.append({files_h[i].getText(),files_p[i].getText()})

for dat in data:
    print(dat)

# tab 7 => terminal
    # all of it
# tab 8 => story
    # all of it
# tab 9 => voice
    # all of it
# tab 10 => skin(optional only one who have skin)
    # all of it
with open('./testing.txt','w') as x:
    i=0
    for tab in tabs:
        x.write('----{count}-----\n\n'.format(count=i))
        i+=1
        x.write(tab.prettify())
driver.close()