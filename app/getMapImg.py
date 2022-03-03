import re
import requests
from bs4 import BeautifulSoup
import os
import errno
from dotenv import load_dotenv


load_dotenv()

dataPath = os.environ["BRAWL_COACH_DATAPATH"]
frontPath = os.environ["BRAWL_COACH_FRONTPATH"]
backPath = os.environ["BRAWL_COACH_BACKPATH"]
logPath = os.environ["BRAWL_COACH_LOGPATH"]
token = os.environ["BRAWL_COACH_TOKEN"]
currentBattlePath = dataPath+"/battles/current"
allBattlePath = dataPath+"/battles/all"
webImgPath = frontPath+"/app/static/img"


sites = ['https://brawlify.com/gamemodes/detail/Duels', 
'https://brawlify.com/gamemodes/detail/Hot-Zone', 
'https://brawlify.com/gamemodes/detail/Knockout', 
'https://brawlify.com/gamemodes/detail/Gem-Grab', 
'https://brawlify.com/gamemodes/detail/Showdown', 
'https://brawlify.com/gamemodes/detail/Duo-Showdown', 
'https://brawlify.com/gamemodes/detail/Bounty', 
'https://brawlify.com/gamemodes/detail/Brawl-Ball', 
'https://brawlify.com/gamemodes/detail/Siege',
'https://brawlify.com/gamemodes/detail/Heist',
'https://brawlify.com/gamemodes/detail/Super-City-Rampage',
'https://brawlify.com/gamemodes/detail/Wipeout']

modes=["DUELS", "HOTZONE", "KNOCKOUT", "GEMGRAB", "SOLOSHOWDOWN", "DUOSHOWDOWN", "BOUNTY", "BRAWLBALL", "SIEGE", "HEIST", "SUPERCITYRAMPAGE", "WIPEOUT"]
#site = "https://brawlify.com/gamemodes/detail/Duels"
i=0
for site in sites:
    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]

    for url in urls:
        if ".png" in url:
            filename=url.split("/")[-1]
            print(filename)
            print(url)
            pictureName=filename.lower()
            pictureName=pictureName.replace("-"," ")
            pictureName=pictureName.replace(" 2","")
            pictureName=pictureName.replace("'","")
            pictureName=pictureName.replace(".png","")
            pictureName=pictureName.replace(".","")
            pictureName=pictureName+".png"
            pictureName=pictureName.replace(" ","")
            if(modes[i]=="DUOSHOWDOWN"):
                pictureName=pictureName.replace("duo","")
                
            print(pictureName)

            filename=webImgPath+"/maps/"+modes[i].lower()+"/"+pictureName
            print(filename)
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            with open(filename, 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative 
                    # if it is provide the base url which also happens 
                    # to be the site variable atm. 
                    url = '{}{}'.format(site, url)
                response = requests.get(url)
                f.write(response.content)
    i=i+1