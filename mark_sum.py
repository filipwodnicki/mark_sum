import sys
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words
import markdown_generator as mg

LANGUAGE = "english"
SENTENCES_COUNT = 3


# Beautiful Soup functions
def get_soup(url):
	"""returns the BeautifulSoup soup"""
	r = requests.get(url)
	soup = BeautifulSoup(r.text, features="lxml")
	return soup

def get_h1(soup):
	"""returns text located with <h1> tag"""
	soup_h1 = soup.find('h1').get_text()
	return soup_h1

def get_img_after_h1(soup):
	"""returns src attribute (aka URL) of the first <img> after <h1>"""
	soup_h1 = soup.find('h1')
	soup_img_url = soup_h1.find_next('img').get('src')
	return soup_img_url

def get_all_img_after_h1(soup):
	"""returns list of all <img> after <h1> including all attributes """
	soup_h1 = soup.find('h1')
	soup_imgs = soup_h1.find_all_next('img', width=True, height=True)
	return soup_imgs

def get_largest_image_from_list(list_of_img):
	"""returns the largest image in a soup list, based on area (height*width)"""
	images = []
	sizes = []
	for img in list_of_img:
		images.append(img.get('src'))
		sizes.append(int(img.get('width')) * int(img.get('height')) )

	if len(sizes) > 0:
		max_size = max(sizes)
		max_index = sizes.index(max_size)
		largest_image = images[max_index]
		return largest_image
	else:
		return None

if __name__ == '__main__':
	url = sys.argv[1] #Get the URL from the first CLI argument
	output_file = sys.argv[2] #Get the markdown filename 

	print("url: ", str(url))

	#Beautiful soup to get Title, Source, Featured Image
	soup = get_soup(url)
	article_title = get_h1(soup)
	print("Title: ", article_title)

	article_source = urlparse(url).hostname
	print("Source: ", article_source)

	if get_all_img_after_h1(soup) != []:
		img_list = get_all_img_after_h1(soup)
		featured_image_url = get_largest_image_from_list(img_list)
	else:
		featured_image_url = get_img_after_h1(soup)

	print("img:", featured_image_url)

	# Sumy setup, use Sumy to get Summary
	parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = Summarizer(stemmer)
	summarizer.stop_words = get_stop_words(LANGUAGE)

	#build a summary (list with sentences as items)
	summary = summarizer(parser.document, SENTENCES_COUNT)

	for sentence in summary:
		print(sentence)

	#Generate markdown
	with open(output_file, 'w') as f: #Markdown-generator setup
		writer = mg.Writer(f)
		
		#Title and Source
		writer.write_heading(article_title)
		writer.write('Source: {}'.format(article_source))
		writer.writeline()
		
		#Image
		image = mg.Image(featured_image_url, article_title)
		writer.writeline(image)
		writer.writeline()
		
		#Summary
		for sentence in summary:
			writer.writeline(sentence)
			writer.writeline()
		
		#Link
		link = mg.link(str(url), 'Full text')
		writer.writeline(link)

	
	


