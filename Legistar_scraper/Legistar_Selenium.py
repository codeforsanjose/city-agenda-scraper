#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      m_noa
#
# Created:     04/05/2021
# Copyright:   (c) m_noa 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# %%
import json
import os
import sys
from datetime import date, timedelta
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
env = json.load(open(os.getcwd() + '/env.json', 'r'))
args = sys.argv

# %%
url = args[1]
# test url for now, later will be list of urls to loop thru
session = HTMLSession()


def use_path(local_path):
    if sys.platform == 'Windows':
        local_path = local_path.replace('/', '\\')
    return env.path + local_path


def set_date(start_date=date.today(), end_date=date.today() + timedelta(days=7)):
    if start_date.month >= date.today().month:
        return 4
# 4 should be the right number of spaces from "last year"

#def set_committee(committee='City Council'):


def scrape_meetings(url):

    driver = webdriver.Firefox()
    driver.get(url)
    WebDriverWait(driver, 5)
    dates = driver.find_elements_by_tag_name('li')
    i = 0
# not sure why we're looking for "Last Week", changed to "Last Year"
    for iter_date in dates:
        if iter_date.text == 'Last Year':
            break
        i += 1
    dates[i + set_date()].click()
    WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_gridCalendar_ctl00'))
    )
    links = []
    elements = driver.find_elements_by_link_text('Meeting details')
    for element in elements:
        link = element.get_attribute('href')
        if link is not None:
            links.append(link)
    for item in links:
        get_agenda(item)

#    pd.read_html(driver.page_source) could be used to take tables in Selenium instead of requests_html

def get_agenda(link):

    header_list = [
    'File #',
    'Staff Report link',
    'Ver.',
    'Agenda #',
    'Agenda Note',
    'Type',
    'Title',
    'Action',
    'Result',
    'Action Details',
    'Video'
    ]
# this is a revised list of headers for the output csv file.

    tables = pd.read_html(link, keep_default_na=False)

    meeting_name = tables[2].iloc[0,1]
# Grabbing meeting name from tables
    target_date = (tables[3].iloc[0,1]).split(' ')[0].replace('/', '-')
# Grabbing meeting date from tables
    tables[11] = tables[11].reindex(columns = header_list)
# This adds a new column to dataframe for the 'Staff Report link'

    l = tables[11]['File #'].tolist()
# Grabs column of File # to find Staff Report hyperlinks
    data = []
    r2 = session.get(link)
# Loads Legistar 'Meeting Details' page

    for item in l:
        if not item:
            # this checks for blank rows with no File # (Staff Report)
            data.append('')
        else:
            report = r2.html.find('a', containing=str(item), first=True)
# Finds hyperlinks from anchor tags
            try:
                data.append(report.attrs.get('href'))
            except:
                data.append('Error')
                continue

    tables[11]['Staff Report link'] = data
    tables[11].to_csv((path + meeting_name + ' ' + target_date + '.csv'), index=False, errors='replace')
# Creates filename with 'Meeting Name' and 'Date'


scrape_meetings(url)
