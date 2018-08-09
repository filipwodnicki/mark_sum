from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.wired.com/2017/08/uncanny-valley-internet/')
soup = BeautifulSoup(r.text)
images = []
for img in soup.findAll('img'):
	images.append(img.get('src'))

print(images)