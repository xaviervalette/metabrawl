from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import json

url="https://brawlstars.fandom.com/wiki/Crossroads"
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



for link in soup.findAll('a'):
    links.append(link.get('href'))

imgLinks = []
for link in links:
    try:
        if("/wiki/" in link):
            imgLinks.append(link)
    except:
        print("Error")
#print(imgLinks)