import sys

from bs4 import BeautifulSoup
import requests

from urllib.parse import urlparse

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 3

import markdown_generator as mg

# Beautiful Soup functions
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
	url = sys.argv[1] #Get the URL from the first CLI argument
	output_file = sys.argv[2] #Get the markdown filename 

	print("url: ", str(url))

	soup = get_soup(url)
	article_title = get_h1(soup)
	print("Title: ", article_title)

	article_source = urlparse(url).hostname
	print("Source: ", article_source)

	featured_image_url = get_img_after_h1(soup)
	print("img:", featured_image_url)

	# Sumy setup
	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	#build a summary (list with sentences as items)
	summary = summarizer(parser.document, SENTENCES_COUNT)

	for sentence in summary:
		print(sentence)

	#Generate markdown
	with open(output_file, 'w') as f:
		writer = mg.Writer(f)
		
		writer.write_heading(article_title)
		writer.write('Source: {}'.format(article_source))
		writer.writeline()
		
		image = mg.Image(featured_image_url, article_title)
		
		writer.writeline(image)
		writer.writeline()
		
		for sentence in summary:
			writer.writeline(sentence)
			writer.writeline()
		
		link = mg.link(str(url), 'Full text')
		writer.writeline(link)

	
	


