#!/usr/bin/python3
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import xml.etree.ElementTree
import os
import time
import urllib.parse
import requests

base_url = "http://www.dr.dk/allepodcast/"
channels_api_url = "https://www.dr.dk/AllePodcast/api/getchannels"
podcast_api_url = "https://www.dr.dk/AllePodcast/api/GetByFirst"
channels = []
browser = Browser('phantomjs')

def encode_channel(c):
	return urllib.parse.quote_plus(c.lower())

def create_url(url=podcast_api_url, letter="", channel=""):
	return url + "?" + urllib.parse.urlencode({
		"letter": letter,
		"channel": channel
	})

def try_int(s):
	try:
		return int(s)
	except:
		return -1

def clear():
	dummy_val = os.system("cls")
	dummy_val = os.system("clear")

def greet():
	print("###################################################################")
	print("# _____  _____     _____ _   _  ____   ____  _____  ______ _____  #")
	print("#|  __ \|  __ \   / ____| \ | |/ __ \ / __ \|  __ \|  ____|  __ \ #")
	print("#| |  | | |__) | | (___ |  \| | |  | | |  | | |__) | |__  | |__) |#")
	print("#| |  | |  _  /   \___ \| . ` | |  | | |  | |  ___/|  __| |  _  / #")
	print("#| |__| | | \ \   ____) | |\  | |__| | |__| | |    | |____| | \ \ #")
	print("#|_____/|_|  \_\ |_____/|_| \_|\____/ \____/|_|    |______|_|  \_\#")
	print("###################################################################")                                                                 
	print("")

def get_podcast_url():
	clear()
	greet()                                                         
	print("Please select a sorting method")
	print("\t(0) Search by name")
	print("\t(1) Search by channel")

	selection = ""
	while selection != "0" and selection != "1":
		selection = input("> ")
	if selection == "0":
		pass
	elif selection == "1":
		print("Loading...")
		channels = requests.get(channels_api_url).json()
		clear()
		greet()
		print("Please select a channel")
		for i in range(len(channels)):
			print("\t({0}) {1}".format(i, channels[i]))
		
		selection = ""
		while try_int(selection) not in range(len(channels)):
			selection = input("> ")
		selected_channel = channels[try_int(selection)]
	return create_url(channel=encode_channel(selected_channel))

def get_podcast_xml_docs(url=podcast_api_url):
	podcasts = []
	json = requests.get(url).json()
	for item in json['Data']:
		xml_source = requests.get(item['XmlLink']).text
		podcasts.append(xml_source)
	return podcasts

def extract_podcasts_from_xml(doc):
	media = []
	root = xml.etree.ElementTree.fromstring(doc)
	items = root[0].findall('item')
	for item in items:
		media.append({
			'title': item[1].text,
			'source': item[4].attrib['url']
		})
	return media

def get_title_from_xml(doc):
	root = xml.etree.ElementTree.fromstring(doc)
	return root[0][0].text

if __name__ == "__main__":
	podcasts = []
	xml_docs = get_podcast_xml_docs(get_podcast_url())
	for i in range(len(xml_docs)):
		podcasts.append({
			"title": get_title_from_xml(xml_docs[i]),
			"xml": xml_docs[i]
		})
	clear()
	greet()
	print("Please select a podcast")
	for i in range(len(podcasts)):
		print("\t\t({0}) {1}".format(i, podcasts[i]['title']))

	selection = -1
	while(try_int(selection) not in range(len(podcasts))):
		selection = input("> ")
	selection = try_int(selection)


	clear()
	greet()
	print("Please select an episode")
	episodes = extract_podcasts_from_xml(podcasts[selection]['xml'])
	for i in range(len(episodes)):
		print("\t\t({0}) {1}".format(i, episodes[i]['title']))

	selection = -1
	while(try_int(selection) not in range(len(episodes))):
		selection = input("> ")
	selection = try_int(selection)

	print(episodes[selection]['title'])