from PIL import Image
import requests
import json
import os
import re
data=[]
with open('./charlist.json') as f:
    data=json.load(f)
finished=[]
for file in os.listdir('./icon'):
    finished.append(re.search('(.*)\.png',str(file)).group(1))
print(finished)
for char in data:
    if(char["char_name"].lower() in finished):
        print("skip {name}".format(name=char["char_name"]))
        continue
    local_filename=char["char_name"].lower()
    linkname=local_filename
    linkname=linkname.replace(" ","")
    linkname=linkname.replace("&","")
    if(linkname=="bennyandcuro"):
        linkname="bennycuro"
    print("{filename} {linkname}".format(filename=local_filename,linkname=linkname ))
    if(char["faction"]!="silent hunter"):
        print("standard image")
        while True:
            try:
                url="https://alchemystars.kloenlansfiel.com/img/alchemy/aurorian/{linkname}.webp".format(linkname=linkname)
                im = Image.open(requests.get(url, stream=True,timeout=20).raw)
                im=im.resize((600,600),Image.ANTIALIAS)
                im.save("./image/"+local_filename+".png",optimize=True,quality=50)
            except:
                print("bruh")
                continue
            break
            

    if(char["char_rarity"]!="3"):
        print("A3")
        while True:
            try:
                url="https://alchemystars.kloenlansfiel.com/img/alchemy/aurorian/{linkname}3.webp".format(linkname=linkname)
                im = Image.open(requests.get(url, stream=True,timeout=20).raw)
                im=im.resize((600,600),Image.ANTIALIAS)
                im.save("./image/"+local_filename+"3.png",optimize=True,quality=50)
            except:
                print("bruh")
                continue
            break
        
    while True:
        try:
            print("logo")
            url="https://alchemystars.kloenlansfiel.com/img/alchemy/logo/{linkname}.webp".format(linkname=linkname)
            im = Image.open(requests.get(url, stream=True,timeout=10).raw)
            im=im.resize((300,150),Image.ANTIALIAS)
            im.save("./icon/"+local_filename+".png",optimize=True,quality=50)
        except:
            print("bruh")
            continue
        break