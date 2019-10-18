from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
import re
import wget
import requests
import shutil

url = "https://www.mdpi.com/1420-3049/24/20/3682/htm"
spliturl = url.split('/', 3)
baseurl = "https://" + spliturl[2]
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()
soup = BeautifulSoup(html_page)
images = []

for img in soup.findAll('img'):
    images.append(img.get('src'))

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

