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

def get_chardata(charname):
    chardata={}
    with open('./json/'+charname+'.json')as f:
        chardata=json.load(f)
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
    skill=tabs[1]
    # skill name  <h4 class="uk-padding-small uk-margin-remove uk-padding-remove">
    chardata['skill']['name']=skill.find('h4',{'class':'uk-padding-small uk-margin-remove uk-padding-remove'}).getText()
    # tab 2 => equip
    equip=tabs[2]
    # equip name
    # print(equip.find('h3').getText())
    # equip description
    chardata['equip']['introduction']=equip.find('p').getText()
    # equip image need download
    url="https://alchemystars.kloenlansfiel.com"+equip.find('img')['data-src']
    print(url)
    im = Image.open(requests.get(url, stream=True,timeout=20).raw)
    im.save("./equip/"+charname+".png",optimize=True,quality=50)
    # tab 3 => collosus
    collosus=tabs[3]
    chardata['collosus']={}
    chardata['collosus']['skill']=[]
    collosus_span=collosus.find_all('span')
    collosus_h=collosus.find_all('h4')
    # skill 1
    chardata['collosus']['skill'].append({'name':(collosus_h[0].getText()),'effect':(collosus_span[0].getText())})
    # skill 2
    chardata['collosus']['skill'].append({'name':(collosus_h[1].getText()),'effect':(collosus_span[1].getText())})
    chardata['collosus']['conversation']=[]
    try:
        conversation=collosus.find_all('ul')
        name=collosus.find_all('div',{'uk-toggle':re.compile('#group-talk-\d+$')})
        count=0
        for ul in conversation:
            talk=ul.find_all('h5')
            speech=ul.find_all('p')
            chats=[]
            for i in range(len(talk)):
                chats.append({'character':talk[i].getText(),'text':speech[i].getText()})
            characters=name[count].find_all('img')
            char=[]
            for character in characters:
                char.append(character['alt'])
            chardata['collosus']['conversation'].append({'character':char,'chat':chats})
            count+=1
    except:
        print("no conversation here")
    chardata['collosus']['furniture']=[]
    try:
        for i in range(len(collosus_h[4:])):
            chardata['collosus']['furniture'].append({'name':collosus_h[i+4].getText(),'description':collosus_span[i+2].getText()})
    except:
        print("no character limited furniture")
    # tab 4 => gift
    gift=tabs[4]
    # find the tag and list it as needed
    gift_list=gift.find_all('p')
    data=[]
    for gf in gift_list[:2]:
        print(gf)
        if(re.search("given to (.* )",gf.getText()).group(1) not in data):
            data.append(re.search("given to (.*)\.",gf.getText()).group(1))
    chardata['gift']=data
    # tab 5 => profile
    profile=tabs[5]
    #description
    spanned_profile=profile.find_all('span')
    for i in range(len(spanned_profile)):
        #nickname
        if(spanned_profile[i].getText()=='Nickname:'):
            chardata['nickname']=(spanned_profile[i+1].getText())
        #gender
        if(spanned_profile[i].getText()=='Gender:'):
            chardata['gender']=(spanned_profile[i+1].getText())
        #height
        if(spanned_profile[i].getText()=='Height:'):
            chardata['height']=(spanned_profile[i+1].getText())
        #birthday
        if(spanned_profile[i].getText()=='Birthday:'):
            chardata['birthday']=(spanned_profile[i+1].getText())
        #birthplace
        if(spanned_profile[i].getText()=='Birthplace:'):
            chardata['birthplace']=(spanned_profile[i+1].getText())
        #fighting style
        if(spanned_profile[i].getText()=='Fighting Style:'):
            chardata['style']=(spanned_profile[i+1].getText())
    # tab 6 => files
    files=tabs[6]
    files_p=files.find_all('p')
    files_h=files.find_all('h4')
    data=[]
    for i in range(len(files_p)):
        data.append({'file_name':files_h[i].getText(),'files':files_p[i].getText()})
    chardata['files']=data
    # for dat in data:
    #     print(dat['file_name'])
    #     print(dat['files'])
    legendary=['Frostfire','Regal','Mythos','Requiem']
    if(charname in legendary):
        voice=tabs[7]
        content_all=voice.find_all('div',{'class':'uk-width-expand'})
        voice_res=[]
        for i in range(len(content_all)):
            voice_res.append(content_all[i].getText())
        chardata['voice']=voice_res
        with open('./json/{charname}.json'.format(charname=charname),'w') as x:
            json.dump(chardata, x, indent = 1)
        return
    # tab 7 => terminal
    # he makes API for this one not much different per se
    noTerminal=['Nails']
    if(charname not in noTerminal):
        terminal=tabs[7]
        # get all button
        chat_button=terminal.find_all('button')
        terminalData=[]
        for butt in chat_button:
            #get the api host then fetch the chat data
            url=butt['onclick']
            url=re.search('\'(.*)\'',url).group(1)
            print(url)
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://alchemystars.kloenlansfiel.com"+url)
            terminal=bs(driver.page_source,'html.parser')
            driver.close()
            tmp={}
            #get the starting dialog
            try:
                li_all=terminal.find('ul')
                li_all=li_all.find_all('li',recursive=False)
            except:
                print('internalError')
                continue
            tmp["start"]=[]
            tmp["branch"]=[]
            for li in li_all:
                if(not li.find('ul')):
                    tmp["start"].append({'name':li.find('h5').getText(),'content':li.find('p').getText()})
                    print(tmp['start'][-1])
                else:
                    tmp["branch"].append({'name':li.find('h5').getText(),'content':li.find('p').getText()})
                    print("branched")
                    print(tmp['branch'][-1])
            ul_all=terminal.find_all('ul')
            ul_all=ul_all[1:]
            tmp["chatlist"]=[]
            #get all the reply with their respective branches
            for ula in ul_all:
                ttmp={}
                li_all=ula.find_all('li',recursive=False)
                ttmp["start"]=[]
                ttmp["branch"]=[]
                for li in li_all:
                    if(not li.find('ul')):
                        ttmp["start"].append({'name':li.find('h5').getText(),'content':li.find('p').getText()})
                        print(ttmp['start'][-1])
                    else:
                        ttmp["branch"].append({'name':li.find('h5').getText(),'content':li.find('p').getText()})
                        # print("branched")
                        print(ttmp['branch'][-1])
                tmp['chatlist'].append(ttmp)
            terminalData.append(tmp)
        # chardata['terminal']=terminalData

    # tab 8 => story
    # need javascript will be implemented another time
    noStory=['Chandra','Alice','Lilliam','Ansia','Sylva','Wendy','Lester','Jola','Pasolo','Korgon','Chainsaw Rick','Pepi','White Dwarf','Unimet','Leah','Clover','Eho']
    if(charname not in noStory):
        if(charname in noTerminal):
            story=tabs[7]
        else:
            story=tabs[8]
        story=story.find('ul')
        story=story.find_all('li')
        chardata['story']=[]
        for li in story:
            storyData={}  
            # title 
            storyData['title']=li.find('h4').getText()
            # header
            print()
            storyData['header']=li.find('p').getText()
            url=li.find('button')['onclick']
            # the chat
            baseurl=re.search('\'(.*)\'',url).group(1)
            baseurl=re.search('(.*\/)\d+',baseurl).group(1)
            maxIndex=0
            j=0
            storyData['chat']=[]
            while(j<=maxIndex):
                print(j,maxIndex)
                driver = webdriver.Chrome(options=chrome_options)
                driver.get("https://alchemystars.kloenlansfiel.com"+baseurl+str(j))
                terminal=bs(driver.page_source,'html.parser')
                h5_all=terminal.find_all('h5')
                p_all=terminal.find_all('p')
                a_all=terminal.find_all('a')
                chat=[]
                branch=[]
                #now we have the terminal of the last one so... get each char name + dialogue
                for i in range(len(p_all)):
                    chat.append({'char':h5_all[i].getText(),'dialogue':p_all[i].getText()})
                # last get the branch and the link
                for a in a_all:
                    aIndex=re.search('\'(.*)\'',a['onclick']).group(1)
                    print(aIndex)
                    aIndex=re.search('.*\/(\d+)$',aIndex).group(1)
                    print(aIndex)
                    branch.append({'text':a.getText(),'link':aIndex})
                    maxIndex=max(int(aIndex),int(maxIndex))
                storyData['chat'].append({'chat':chat,'branch':branch})
                j+=1
            # chardata['story'].append(storyData)
        driver.close()
        # it will result in [] with index of the last url
        
        # now navigation
        # every page have a to navigation and it continue without any key before

    # tab 9 => voice
    if(charname in noTerminal and charname in noStory ):
        voice=tabs[7]
    elif(charname in noTerminal or charname in noStory):
        voice=tabs[8]
    else:
        voice=tabs[9]
    content_all=voice.find_all('div',{'class':'uk-width-expand'})
    voice_res=[]
    for i in range(len(content_all)):
        voice_res.append(content_all[i].getText())
        
    chardata['voice']=voice_res
    # tab 10 => skin(optional only one who have skin)
    skins=None
    try:
        if(charname in noTerminal and charname in noStory ):
            skins=tabs[8]
        elif(charname in noTerminal or charname in noStory):
            skins=tabs[9]
        else:
            skins=tabs[10]   
    except:
        print("no skins")
    skin_data=[]
    chardata['skins']=[]
    if(skins):
        #skin name
        name=skins.find_all('h3')
        #skin description
        description=skins.find_all('p')
        #skin skins
        img=skins.find_all('a',{'class':'full-art-skin'})
        # all of it
        for i in range(len(name)):
            skin_data.append({'name':name[i].getText(),'description':description[i].getText()})
            url="https://alchemystars.kloenlansfiel.com"+img[i]['href']
            print(url)
            while(True):
                try:
                    im = Image.open(requests.get(url, stream=True,timeout=20).raw)
                    im = imageedit.trim(im)
                    im=im.resize((int(im.width*550/im.height),550),Image.ANTIALIAS)
                    im=imageedit.add_margin(im,0,int((700-im.width)/2),0,int((700-im.width)/2),(0,0,0,0))
                    im.save("./image/"+skin_data[i]['name']+".png",optimize=True,quality=50)
                except:
                    print("bruh")
                    continue
                break
        chardata['skins']=skin_data

    with open('./json/{charname}.json'.format(charname=charname),'w') as x:
        json.dump(chardata, x, indent = 1)
    if(charname not in noStory):
        with open('./json/{charname}story.json'.format(charname=charname),'w') as x:
            json.dump(storyData, x, indent = 1)
    if(charname not in noTerminal):
        with open('./json/{charname}terminal.json'.format(charname=charname),'w') as x:
            json.dump(terminalData, x, indent = 1)
    # storyData
    # terminalData