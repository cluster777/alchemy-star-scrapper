from bs4 import BeautifulSoup as bs
import re
def get_data(target): 
    data=[]

    soup=bs(target,'html.parser')
    char_all=soup.find_all('div',{'class':'charInfoBlock'})
    with open('./checkthisout.txt','w') as x:
        x.write(char_all[1].prettify())
    for char in char_all:

        name=char.find_all('div',{'class':'name'})

        #skill=char.find_all('div',{'class':'Skill'})
        skillcd=char.find_all('div',{'class':'SkillCD'})
        #equipdesc=char.find_all('div',{'class':'charEQ'})
        equipname=char.find('div',{'class':'equipName'})
        equippassive=char.find('div',{'class':'passiveName'})
        faction=char.find_all('div',{'class':'Faction'})

        ele_main=char.find_all('div',{'class':'Ele'})
        ele_sub=char.find_all('div',{'class':'Ele2'})
        rarity=char.find_all('div',{'class':'Rarity'})
        cclass=char.find_all('div',{'class':'Role'})

        breaktrought=char.find_all('div',{'class':'charBT'})
        ascensiondetail=char.find_all('div',{'class':'gradeDetail'})

        for i in range(len(name)):
            
            tmp ={}
            #first pattern get the span value in the class
            tmp["name"]=name[i].find('span').getText()
            tmp["faction"]=faction[i].find('span').getText()
            if(tmp["name"] in ["Frostfire","Regal","Requiem","Mythos"]):
                tmp["faction"]="silent hunter"
            print("found character name:{name} from {faction}".format(name=tmp["name"], faction=tmp["faction"]))
            #misc data
            tmp['element_main']=re.search('Ele\d* (\w+)',str(ele_main[i]))
            if tmp['element_main']!=None:
                tmp['element_main']=tmp['element_main'].group(1)

            tmp['element_sub']=re.search('Ele\d* (\w+)',str(ele_sub[i]))
            if tmp['element_sub']!=None:
                tmp['element_sub']=tmp['element_sub'].group(1)

            tmp['rarity']=re.search('Rarity(\d)',str(rarity[i]))
            if tmp['rarity']!=None:
                tmp['rarity']=tmp['rarity'].group(1)
            
            tmp['class']=re.search('Role (\w+)',str(cclass[i]))
            if tmp['class']!=None:
                tmp['class']=tmp['class'].group(1)
            
            
            #skill
            tmp["skill"]={}
            tmp["skill"]["name"]=""
            tmp["skill"]["cd"]=skillcd[i].find('span').getText()
            #need description for each ascension(1x3)(ascend (0,1),2,3)

            #equip
            tmp["equip"]={}
            tmp["equip"]["name"]=equipname.find('span').getText()
            tmp["equip"]["passive"]=equippassive.find('span').getText()
            #need equip description for each ascension(4x3)(ascend 1,2,3)
            
            #chain combo
            tmp["chain"]={}
            tmp["chain"]["name"]=""
            #need description and cost for each ascension (3x3)(ascend (0,1),2,3)

            #third patern
            tmp['breaktrought']=[]
            #for each bt i must store the span inside
            for bt in breaktrought:
                tmp['breaktrought'].append(bt.find('span').getText())

            tmp["ascension"]=[]
            for detail in ascensiondetail:
                if(tmp["faction"]=="silent hunter"):
                    break
                ttmp={}
                material=detail.find_all('span',{'class':'item'})
                if(not material):
                    break
                ascensiontype=detail.find('div',{'class': re.compile("upgrade\d")})
                ascensionbefore=detail.find('div',{'class': re.compile("upgradeB\d")})
                ascensionafter=detail.find('div',{'class': re.compile("upgradeA\d")})
                ttmp["material"]=[]
                for mat in material:
                    
                    ttmp["material"].append(mat.find('span',{'class':'itemName'}).getText())
                ttmp["type"]=re.search('(.*) U',ascensiontype.find('span').getText()).group(1)
                if(ascensionbefore):
                    ttmp["before"]=ascensionbefore.find('span').getText()
                if(ascensionafter):
                    ttmp["after"]=ascensionafter.find('span').getText()
                tmp["ascension"].append(ttmp)
            data.append(tmp)

    return data
def get_stat(target,rarity,asc):
    soup=bs(target,'html.parser')
    char_stat=soup.find('div',{'id':'info'}).find('div',{'class':'detailsCol'})
    att=char_stat.find('div',{'class':'ATK'}).find('span').getText()
    defen=char_stat.find('div',{'class':'DEF'}).find('span').getText()
    hp=char_stat.find('div',{'class':'HP'}).find('span').getText()
    equipatt=0
    equipdef=0
    equiphp=0
    if(asc>0):
        if(rarity>=5):
            equipatt=30
            equipdef=10
            equiphp=50
        else:
            equipatt=25
            equipdef=10
            equiphp=50

    return {"att":int(att)-int(equipatt),"def":int(defen)-int(equipdef),"hp":int(hp)-int(equiphp)}
# move this to the masterpiece and do it for every ascension
def get_chain(target):

    soup=bs(target,'html.parser')
    soup=soup.find('div',{'id':'info'})
    ccx=soup.find_all('div',{'class':'overviewDetail'})[1]
    
    tmp=[]

    ccx=ccx.find_all('div',{'class':re.compile('CD\dA\d')})

    for cc in ccx:
                ttmp={}
                #get the cost
                ttmp['cost']=re.search('charAbility TP(\d+)',str(cc))
                if ttmp['cost']!=None:
                    ttmp['cost']=ttmp['cost'].group(1)

                #get the description
                ttmp['description']=cc.find('span')
                if ttmp['description']!=None:
                    ttmp['description']=ttmp['description'].getText()
                
                tmp.append(ttmp)
    
    #tmp["skill"]["description"]=active.find('div',{'class':'Equipment'}).find('span').getText()
    return tmp

def get_skill(target):
    soup=bs(target,'html.parser')
    soup=soup.find('div',{'id':'info'})
    active=soup.find_all('div',{'class':'overviewDetail'})[0]
    return active.find('div',{'class':'Skill'}).find('span').getText()

def get_equip(target):
    soup=bs(target,'html.parser')
    soup=soup.find('div',{'id':'info'})
    active=soup.find_all('div',{'class':'overviewDetail'})[0]
    return active.find('div',{'class':'Equipment'}).find('span').getText()

#print(data)