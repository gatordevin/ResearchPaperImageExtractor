from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
import re
import wget
import requests
import shutil
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap

url = "https://www.mdpi.com/1420-3049/24/20/3682/htm"
spliturl = url.split('/', 3)
baseurl = "https://" + spliturl[2]
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()
soup = BeautifulSoup(html_page)
images = []
captions = []

for img in soup.findAll('img'):
    if(img.parent.name == "div"):
        try:
            captions.append(img.parent.parent.parent.find("div",{"class": "html-fig_description"}).text)
        except:
            captions.append("")
        images.append(img.get('src'))

mydivs = soup.findAll("div", {"class": "html-fig_description"})
for div in mydivs:
    #print(div)
    None

count = 0
for img in images:
    if img != None:
        count += 1
        if("https://" not in img):
            img = baseurl + img
        r = requests.get(img, stream=True)
        if r.status_code == 200:
            with open(str(count) + ".png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            img = Image.open(str(count) + ".png")
            draw = ImageDraw.Draw(img)
            margin = offset = 20
            for line in textwrap.wrap(str(captions[count-1].encode("utf-8").decode('latin-1')), width=img.width/7):
                draw.text((margin, offset), line)
                offset += 10
            img.save(str(count) + ".png")

