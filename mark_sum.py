import sys

from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

from bs4 import BeautifulSoup
import requests

LANGUAGE = "english"
SENTENCES_COUNT = 3

def get_all_images(url):
	images = []
	r = requests.get(url)
	soup = BeautifulSoup(r.text, features="lxml")
	for img in soup.findAll('img', width=True, height=True):
		images.append(img.get('src'))
	return images

if __name__ == '__main__':
	url = sys.argv[1]
	print("Type of url: ", type(url))
	print("url: ", str(url))
	# url = "https://www.bbc.com/news/business-45105674"
	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	for sentence in summarizer(parser.document, SENTENCES_COUNT):
		print(sentence)

	print ( get_all_images(url) )


