from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json
import requests
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


baseUrl = "https://brawlstars.fandom.com/wiki"
url=f"{baseUrl}/Crossroads"

"""
GET MAPS PER MODES TABLE
"""
mapsPerModesDict = {}
req = Request(url)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
data = []
for table in soup.findAll('table', class_="navbox parent-navbox"):

    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        try:
            rowTitles = row.find_all('th')
            mode = rowTitles[0].text.replace("\n","")
            cols = row.find_all('td')
            maps = cols[0].text.replace("\n","")
            maps=maps.split(" • ")
            mapsClean = []
            for map in maps:
                map=map.replace(f" ({mode})","")
                mapsClean.append(map)
            mapsPerModesDict[mode]=mapsClean
        except:
            print("ERROR")

print(mapsPerModesDict)
with open('mapsPerModes.json', 'w') as json_file:
  json.dump(mapsPerModesDict, json_file, indent=4)


"""
GET MAP IMAGES
"""
for mode in mapsPerModesDict:
    for map in mapsPerModesDict[mode]:
        print(map)
        imgUrl=f"{baseUrl}/{map.replace(' ', '_')}"
        print(imgUrl)

        try:
            response = requests.get(imgUrl)
            req = Request(imgUrl)
            html_page = urlopen(req)
            soup = BeautifulSoup(html_page, "lxml")
            imgHtml=soup.findAll("img")
            print(imgHtml[1]["src"])
            filePath = f"{webImgPath}/maps/originalImg/{mode.replace(' ','').lower()}/{map.replace(' ', '').replace('-', '').replace('.', '').lower()}.png"
            if not os.path.exists(os.path.dirname(filePath)):
                try:
                    os.makedirs(os.path.dirname(filePath))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(filePath, 'wb') as f:
                response = requests.get(imgHtml[2]["src"])
                f.write(response.content)
        except:
            print("ERROR")