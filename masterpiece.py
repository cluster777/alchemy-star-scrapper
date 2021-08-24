from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import fetch
import generator
# choose chrome
driver = webdriver.Chrome()
# slow start
time.sleep(10)
#get the page
driver.get("https://vice-as.herokuapp.com/db/")
# note slow connection thanks
time.sleep(10)

driver.find_element_by_id('btnGradeView').click()
time.sleep(10)
driver.find_element_by_id('btnEquipView').click()
time.sleep(20)
#scrap the main page for general purpose data
data=fetch.get_data(driver.page_source)
generator.generate_charlist(data)
for char in data:
    driver.get("https://vice-as.herokuapp.com/db/"+char["name"])
    time.sleep(10)
    level =  driver.find_element_by_class_name("charLevel")
    ascension=driver.find_element_by_id('info').find_element_by_class_name("charGrade")
    move = ActionChains(driver)
    max=30
    driver.execute_script("document.getElementsByClassName(\"charLevel\")[0].value=2")
    if(char["faction"]!="silent hunter"):
        driver.execute_script("document.getElementById('info').getElementsByClassName(\"charGrade\")[0].value=1")
        ascension.send_keys(Keys.LEFT)
    time.sleep(1)
    level.send_keys(Keys.LEFT)
    print("t")
    char["base_stat"]={}
    char["base_stat"]["stat"]=[]
    time.sleep(1)
    while True:
        #get data init
        char["base_stat"]["stat"].append(fetch.get_stat(driver.page_source,int(char["rarity"]),int(ascension.get_attribute("value"))))
        
        while(int(level.get_attribute("value"))<int(max)):
            #while not max lv add the lv and get the data
            level.send_keys(Keys.ARROW_UP)
            
            char["base_stat"]["stat"].append(fetch.get_stat(driver.page_source,int(char["rarity"]),int(ascension.get_attribute("value"))))
        
        #get value here cc active equipment
        print("datadatadata")
        if(int(max)>70 or (int(char["rarity"])==3 and int(max)>45)):
            generator.generate_char(char)
            break
        #javascript do value set
        driver.execute_script("document.getElementsByClassName(\"charLevel\")[0].value=2")

        level.send_keys(Keys.LEFT)
        if(char["faction"]!="silent hunter"):
            ascension.send_keys(Keys.RIGHT)
        max=level.get_attribute("max")
        time.sleep(1)
    

driver.close()