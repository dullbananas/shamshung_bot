from html.parser import HTMLParser
import requests


class ImageExtractor(HTMLParser):
	urls = []
	def handle_starttag(self, tag, attrs):
		if tag == 'img' and 'src' in attrs.keys():
			self.urls.append(attrs['src'])


def read_webpage(url):
	return requests.get(url).text
