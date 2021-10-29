# Alchemy star scrapper # 
a python program to scrap your needed data of alchemy stars

this program run using python selenium and beautiful soup to scrap the data. 

## How to use ##
install python from [here](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)
for **window** user dont forget to **tick** add to environtment checkbox

nex we need to install depedency we will use pip for this step:
to install pip use this command on command prompt(cmd or terminal)
```
python get-pip.py
```

next install the python depedency using
```
pip install bs4 selenium webdriver-manager
```

now we are ready to take the data
first use create folders named:
* equip
    * this will contain the equipment images from imageIcon
* icon
    * this will contain character's icons from imageIcon
* image
    * this will contain character's skins,ascension0, ascension3 from imageIcon
* json
    * this will contain the character's data it will separated into 3 file
        1. one with the characterName will contain most character data
        1. the other will contain their respective data according to their name terminal or story data
        1. and lastly we have charlist.json it will contain all character short data

next we will run `masterpiece.py` this will take and create file of the character data then save it on json folder this include:
1. one with the characterName will contain most character data
1. and lastly we have charlist.json it will contain all character short data

next we run `imageIcon.py` it will take the other data including:
1. all image,icon and equipment
1. fill the blank in character's json file
1. create character's story and terminal json file