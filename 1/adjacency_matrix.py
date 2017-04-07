import requests
from bs4 import BeautifulSoup
import urllib
import urlparse
import numpy as np

base_url = 'https://ru.wikipedia.org'
use_only_inner_links = True
number_of_links = 100

r = requests.get(base_url)

soup = BeautifulSoup(r.text, 'html.parser')

def has_ru_wiki_ref(tag):
	return tag.has_attr('href') and tag.get('href').startswith(r'/wiki/')

def has_href(tag):
	return tag.has_attr('href')

def filter_links(tag):
	if use_only_inner_links:
		return has_ru_wiki_ref(tag)
	else:
		return has_href(tag)

all_links = soup.find_all(filter_links)

n_links = all_links[:number_of_links]
links_matrix = []

# for link in all_links:
# 	print urllib.unquote(str(link.get("href")))

def encode_url(url):
	return urllib.unquote(str(url))

def process_link(link):
	request = requests.get(base_url + link.get('href'))
	soup = BeautifulSoup(request.text, 'html.parser')
	all_links = soup.find_all(filter_links)
	inner_list = []

	for start_a in n_links:
		if start_a in all_links:
			inner_list.append(1)
			print 'links', encode_url(start_a.get("href"))
		else:
			inner_list.append(0)

	links_matrix.append(inner_list)
	print 'length =', str(len(inner_list))


for i in range(len(n_links)):
	print '===== VISIT: ', str(i), encode_url(n_links[i].get('href'))
	process_link(n_links[i])

# remove selflinks
for i in range(len(n_links)):
	n_links[i][i] = 0

for arr in links_matrix:
	for el in arr:
		print el,
	print '\n'
