# Code for San Jose
# Project: City Agenda Scraper
# Summary: JS Parser Demo

# Import module for Jupyter Notebook
# !pip install requests_html
# Note: dryscrape requires webkit-driver library
# https://dryscrape.readthedocs.io/en/latest/installation.html
# !sudo apt-get install qt5-default libqt5webkit5-dev build-essential \
#                   python-lxml python-pip xvfb
# !pip install dryscrape
# !pip install bs4
import dryscrape
from bs4 import BeautifulSoup

# Javascript parsing demo using the dryscrape package:
# Usage: Adapt code for parsing SJ agenda website
# https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
def js_demo(url):
    dryscrape.start_xvfb()
    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    soup = BeautifulSoup(response)
    soup.find(id="input#ctl00_ContentPlaceHolder1_lstYears_Input.rcbInput.radPreventDecorate")
    # Result:
    # <p id="intro-text">Yay! Supports javascript</p>

# Set URL and pass to function
url = 'https://sanjose.legistar.com/Calendar.aspx'
js_demo(url)
