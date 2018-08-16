import sys

from bs4 import BeautifulSoup
import requests

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 3

def get_soup(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, features="lxml")
	return soup

# def get_all_images(url):
# 	images = []
# 	for img in get_soup(url).findAll('img', width=True, height=True):
# 		images.append(img.get('src'))
# 	return images

def get_h1(soup):
	soup_h1 = soup.find('h1').get_text()
	return soup_h1


def get_img_after_h1(soup):
	soup_h1 = soup.find('h1')
	soup_img_url = soup_h1.find_next('img').get('src')
	return soup_img_url

if __name__ == '__main__':
	url = sys.argv[1]
	# print("Type of url: ", type(url))
	print("url: ", str(url))
	# url = "https://www.bbc.com/news/business-45105674"

	soup = get_soup(url)
	title = get_h1(soup)
	print("Title: ", title)

	featured_image_url = get_img_after_h1(soup)
	print("img:", featured_image_url)


	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	summary = summarizer(parser.document, SENTENCES_COUNT)

	for sentence in summary:
		print(sentence)



	
	


