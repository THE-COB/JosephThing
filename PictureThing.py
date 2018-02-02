from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import shutil
from PIL import Image
import re

# def remWM(fName):
# 	img = Image.open(fName)
# 	rgbImg = img.convert("RGB")
# 	r,g,b = rgbImg.getpixel((50,1))
# 	print(r,g,b)
# 	rgbImg.show()

r = requests.get("http://www.danledbetterphotography.com/p945001994")
fullHtml = r.text
soup = BeautifulSoup(fullHtml, "html.parser")
picCodes = soup.find_all(property="og:image")
pCodeStrs = []
for i in picCodes:
	pCodeStrs.append(str(i))
picLinks = []
for i in pCodeStrs:
	pSoup = BeautifulSoup(i, "html.parser")
	picLinks.append(str(pSoup.meta["content"]))
smallPics = []
for i in picLinks:
	loc = re.search("3.jpg", i)
	startLoc = loc.span()
	smallPics.append(i.split("3.jpg")[0]+"1.jpg")

for i in range(0,len(picLinks)):
	newImg = requests.get(picLinks[i], stream=True)
	with open("BigPics/"+str(i)+".jpg", "wb") as outFile:
		shutil.copyfileobj(newImg.raw, outFile)
	newImg = requests.get(smallPics[i], stream=True)
	with open("SmallPics/"+str(i)+".jpg", "wb") as outFile:
		shutil.copyfileobj(newImg.raw, outFile)
	del newImg
	percent = (i+1)/len(picLinks)
	percent*=100
	print(str(percent)+"%")

