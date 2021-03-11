# Code for San Jose
# Project: City Agenda Scraper
# Summary: JS Parser Demo

# Import modules for Jupyter Notebook
# !pip install requests_html

# Import modules for dryscape library
# Note: dryscrape requires webkit-driver library
# https://dryscrape.readthedocs.io/en/latest/installation.html
# !sudo apt-get install qt5-default libqt5webkit5-dev build-essential \
#                   python-lxml python-pip xvfb
# !pip install dryscrape
# !pip install bs4
# import dryscrape
# from bs4 import BeautifulSoup

# Javascript parsing demo using the dryscrape package:
# Usage: Adapt code for parsing SJ agenda website
# https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
def demo_dryscape(url):
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
# demo_dryscape(url)

# Javascript parsing demo using the selenium package:
# Usage: Adapt code for parsing SJ agenda website
# https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
!pip install selenium
from selenium import webdriver
driver = webdriver.PhantomJS()
driver.get(my_url)
p_element = driver.find_element_by_id(id="input#ctl00_ContentPlaceHolder1_lstYears_Input.rcbInput.radPreventDecorate")
print(p_element.text)
# result:
# 'Yay! Supports javascript'
