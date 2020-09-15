# yellowpagesscrape
This is a web scraper I built with python beautiful soup to scrape leads from yellowpages.com.
I built this project to build a list of businesses to call in my sales career. 

When you run the code it will ask you for two things:
  1. What are you looking for
    - works with one or two word searches. No more than two. 
  2. Where
    - I haven't tested this with cities that have multiple names (San Diego, New York, etc.).
    
It outputs the lists generated in the shell and it also saves it as a .csv file in the directory. 
Adding outgoing emails would be fairly simple to add. 

Libaries used:
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import lxml
