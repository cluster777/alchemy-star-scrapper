from PIL import Image
import requests
import json
import os
import re
import imageedit

data=[]
# make folder called image and another one called icon to make this work
# this program use PIL to compress the image from kloansfiel to save space and loading problem on website
# note pls install PIL if you dont have using pip install PIL

# to get charlist check masterpiece.py to get the file and another note pls delete the last comma on the file if error occur
with open('./charlist.json') as f:
    data=json.load(f)
finished=[]

for file in os.listdir('./icon'):
    finished.append(re.search('(.*)\.png',str(file)).group(1))
#list of finished file checked by the icon on icon folder
print(finished)

for char in data:
    #for each chardata 
    if(char["char_name"].lower() in finished):
        print("skip {name}".format(name=char["char_name"]))
        continue

    #special case and naming convention of kloansfiel site
    local_filename=char["char_name"].lower()
    linkname=local_filename
    linkname=linkname.replace(" ","")
    linkname=linkname.replace("&","")
    if(linkname=="bennyandcuro"):
        linkname="bennycuro"
    
    #debuging stuff and pointer which character that will be get
    print("{filename} {linkname}".format(filename=local_filename,linkname=linkname ))

    #fetch character standard art from kloansfiel site as stated on url 
    if(char["faction"]!="silent hunter"):
        print("standard image")
        while True:
            try:
                url="https://alchemystars.kloenlansfiel.com/img/alchemy/aurorian/{linkname}.webp".format(linkname=linkname)
                im = Image.open(requests.get(url, stream=True,timeout=20).raw)
                im = imageedit.trim(im)
                im=im.resize((int(im.width*550/im.height),550),Image.ANTIALIAS)
                im=imageedit.add_margin(im,0,int((700-im.width)/2),0,int((700-im.width)/2),(0,0,0,0))
                im.save("./image/"+local_filename+".png",optimize=True,quality=50)
            except:
                print("bruh")
                continue
            break

            
    #fetch A3 art from kloansfiel site as stated on url 
    if(char["char_rarity"]!="3"):
        print("A3")
        while True:
            try:
                url="https://alchemystars.kloenlansfiel.com/img/alchemy/aurorian/{linkname}3.webp".format(linkname=linkname)
                im = Image.open(requests.get(url, stream=True,timeout=20).raw)
                im = imageedit.trim(im)
                im=im.resize((int(im.width*550/im.height),550),Image.ANTIALIAS)
                im=imageedit.add_margin(im,0,int((700-im.width)/2),0,int((700-im.width)/2),(0,0,0,0))
                im.save("./image/"+local_filename+"3.png",optimize=True,quality=50)
            except:
                print("bruh")
                continue
            break
        
    #fetch logo from kloansfiel site as stated on url 
    print("logo")
    while True:
        try: 
            url="https://alchemystars.kloenlansfiel.com/img/alchemy/logo/{linkname}.webp".format(linkname=linkname)
            im = Image.open(requests.get(url, stream=True,timeout=10).raw)
            im=im.resize((300,150),Image.ANTIALIAS)
            im=imageedit.add_margin(im,75,0,75,0,(0,0,0,0))
            im.save("./icon/"+local_filename+".png",optimize=True,quality=50)
        except:
            print("bruh")
            continue
        break