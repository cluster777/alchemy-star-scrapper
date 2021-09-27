from bs4 import BeautifulSoup as bs
import re
from PIL import Image
import requests
import json

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
    # conversation if available
    # furniture if available
# tab 4 => gift
    # all of it
# tab 5 => profile
    # all of it
# tab 6 => files
    # all of it
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