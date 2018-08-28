import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def main(line):
	op = ""
	query = line
	url = 'https://en.wikipedia.org/wiki/'+query
	site = urllib.request.urlopen(url)
	html = site.read()
	soup = BeautifulSoup(html,"html.parser")
	res = [i.text.replace('\n', ' ').strip() for i in soup.find_all('p')]
	x = min(4, len(res))
	for iter in range(len(res)):
		op = op + res[iter] + '\n'
	result = op.split('.')
	fop = ""
	for iter in range(x):
		fop = fop + result[iter] + '.'

	fop = re.sub(r"\[[^\]]\]", "", fop)
	return fop