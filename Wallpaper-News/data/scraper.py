import requests
import bs4
from string import Template

class DataScraper:
	def __init__(self):
		# The URLs where the data is scraped from 
		self.LOCAL_NEWS_URL = "https://myrepublica.nagariknetwork.com/category/society"
		self.INT_NEWS_URL = "https://www.nytimes.com/section/world/asia" #any url from the nytimes should work
		self.REDDIT_URL = ""

		# Template for uniform return format
		'''
			index ->  Number (starts from 1)
			data  ->  The Text/News scraped from the URL
		'''
		self.return_format = Template("$index. $data")

	# handle localnews
	def localnews(self):
		titles = list()

		_response = bs4.BeautifulSoup(requests.get(self.LOCAL_NEWS_URL).text,features="lxml")

		for index,articles in enumerate(_response.body.find_all("h2")[2:-2]): # the first and last two items are not news.
			titles.append(self.return_format.substitute({"index":index+1,"data":articles.text}))
		
		return titles

	# handle International news 
	def int_news(self):
		titles = list()

		_response = bs4.BeautifulSoup(requests.get(self.INT_NEWS_URL).text,features="lxml")
		
		for index,articles in enumerate(_response.body.find_all("h2")[:-2]): # the first and last two items are not news.
			titles.append(self.return_format.substitute({"index":index+1,"data":articles.text}))
		
		return titles
