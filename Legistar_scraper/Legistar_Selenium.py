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
import os
import sys
from datetime import date, timedelta
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
full_path = os.environ.get('full_path')
current_city = sys.argv[1]

# %%
session = HTMLSession()


def set_date(start_date=date.today(), end_date=date.today() + timedelta(days=7)):
    if start_date.month >= date.today().month:
        return 4
# 4 should be the right number of spaces from "last year"

#def set_committee(committee='City Council'):


def scrape_meetings(url):

    driver = webdriver.Firefox()
    driver.get("https://%s.legistar.com/Calendar.aspx" %(url))
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_tdYears')))
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_tdYears').click()
    dates = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstYears_DropDown')
    for i, val in enumerate(dates.find_elements_by_tag_name('li')):
        if val.text == 'Last Month':
            dates[i].click()
            break
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_gridCalendar_ctl00')))
    for element in driver.find_elements_by_link_text('Meeting details'):
        link = element.get_attribute('href')
        if link is not None:
            get_agenda(link)

#    pd.read_html(driver.page_source) could be used to take tables in Selenium instead of requests_html

def get_agenda(link):

    header_list = [ 'File #', 'Staff Report link', 'Ver.', 'Agenda #', 'Agenda Note', 'Type', 'Title', 'Action', 'Result', 'Action Details', 'Video' ]
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
    tables[11].to_csv((full_path + meeting_name + '_' + target_date + '.csv'), index=False, errors='replace')
# Creates filename with 'Meeting Name' and 'Date'


scrape_meetings(current_city)
