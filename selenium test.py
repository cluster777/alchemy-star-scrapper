#selenium test
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome()
# note slow startup thanks
time.sleep(5)
driver.get("https://vice-as.herokuapp.com/db/victoria")
# note slow connection thanks
time.sleep(10)

level =  driver.find_element_by_class_name("charLevel")
ascension=driver.find_element_by_id('info').find_element_by_class_name("charGrade")
move = ActionChains(driver)
max=30
driver.execute_script("document.getElementsByClassName(\"charLevel\")[0].value=2")
driver.execute_script("document.getElementById('info').getElementsByClassName(\"charGrade\")[0].value=1")
time.sleep(1)
level.send_keys(Keys.LEFT)
print("t")
ascension.send_keys(Keys.LEFT)
time.sleep(1)
while True:
    #while not max
    while(int(level.get_attribute("value"))<int(max)):
        level.send_keys(Keys.ARROW_UP)
        time.sleep(1)
    #javascript do value set
    driver.execute_script("document.getElementsByClassName(\"charLevel\")[0].value=2")
    level.send_keys(Keys.LEFT)
    time.sleep(1)
    ascension.send_keys(Keys.RIGHT)
    max=level.get_attribute("max")
    time.sleep(1)
    

