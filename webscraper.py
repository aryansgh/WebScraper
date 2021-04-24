import requests
from bs4 import BeautifulSoup
import time
from time import sleep
import pandas as pd
from tabulate import tabulate
from multiprocessing import Pool
from multiprocessing import cpu_count
import concurrent.futures
from functools import lru_cache 
import pickle
import os
import datetime
from datetime import date


site_1 = input("Please enter the url of the site:")

t0=time.time()

contents_list = []

sitemap_url = []

key_list= ["Website Name", "H1 TAG", "H2 TAG", "TITLE", "IMG-ALT"]

dicts_list = {}

MAX_THREADS = 10

for i in key_list:
	dicts_list[i] = []
#getting all the tags and storing it in a list called contents_list

def webscrape(t):
	#print(t)
	#for site_url in sitemap_url:
	#print(site_url)
	request_1 = requests.get(t)
	src_1 = request_1.content
	soup_1  = BeautifulSoup(src_1, 'html.parser')
	h1_list = []
	h2_list = []
	title_list = []
	img_list = []
	for h1 in soup_1.find_all("h1"):
		if None in h1:
			h1_list.append(None)
		else: 
			h1_list.append(h1.text)
	for h2 in soup_1.find_all("h2"):
		if None in h2:
			h2_list.append(None)
		else:
			h2_list.append(h2.text)
	for title in soup_1.find_all("title"):
		if None in title:
			title_list.append(None)
		else:
			title_list.append(title.text)
	for img1 in soup_1.find_all("img"):
		if img1.has_attr('alt'):
			img_list.append(img1['alt'])
	dicts_list["Website Name"].append(t) 
	dicts_list["H1 TAG"].append(h1_list) 
	dicts_list["H2 TAG"].append(h2_list) 
	dicts_list["TITLE"].append(title_list) 
	dicts_list["IMG-ALT"].append(img_list)
	print("done")

#caching function to check if the website has been scarped before
def cache_to_disk(func):
    def wrapper(*args):
        cache = '.{}{}.pkl'.format(func.__name__, args).replace('/', '_')
        try:
            with open(cache, 'rb') as f:
            	time_created2 = os.stat(cache).st_mtime
            	date_time = datetime.datetime.fromtimestamp(time_created2)
            	now = datetime.datetime.today()
            	delta  = now - date_time
            	print("modified date "+ str(date_time))
            	print("today's date: "+ str(now))
            	print(delta.days)
            	days = delta.days 
            	if days>0:
                	print("A")
                	result = func(*args)
                	with open(cache, 'wb') as g:
                		pickle.dump(result, g)
                	return result

            	print("B")
            	t3 = time.time()
            	print(args)
            	print("This site has been scraped before")
            	total_time = t3-t0
            	print("The total time for scraping" + " " + str(total_time))
            	return pickle.load(f)     		 		
        except IOError:
            result = func(*args)
            with open(cache, 'wb') as f:
                pickle.dump(result, f)
            return result

    return wrapper

#Funtion to recursively get all the links of the sitemap
def get_links(url):
	response = requests.get(url)
	src_2 = response.content
	soup_get_links = BeautifulSoup(src_2, 'html.parser')
	local_links = []

	for links in soup_get_links.find_all('loc'):
		link_url = links.text

		if link_url is  not  None: 
			if link_url not in sitemap_url:
				sitemap_url.append(link_url) 
				get_links(link_url)
				print(link_url)


@cache_to_disk
def multipro(site_string):
	site_string = str(site_1)
	get_links(site_string)

	t2 = time.time()
	threads = min(MAX_THREADS, len(sitemap_url))

	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
		executor.map(webscrape, sitemap_url)


	t1=time.time()
	total_time=t1-t2
	total_time2=t1-t0
	print(site_string)
	print("The total time for web scraping is" + " " + str(total_time))
	print("The total time with recursion is" + " " + str(total_time2))
	return dicts_list

def main():
	site_string = str(site_1)

	temp_dict_list = multipro(site_string)

	df = pd.DataFrame(temp_dict_list)
	df.to_html("data.html")

	#webscrape()

main()
