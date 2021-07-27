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
from Gdrive_upload_methods import drive_upload, drive_launch


drive = drive_launch()
full_path = os.environ.get('full_path')
current_city = sys.argv[1]
time_period = sys.argv[2]
meeting_type = sys.argv[3]

session = HTMLSession()


def scrape_meetings(url):

    driver = webdriver.Firefox()
    driver.get("https://%s.legistar.com/Calendar.aspx" %(url))
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_tdYears')))
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_tdYears').click()
    dates = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstYears_DropDown')
    for val in dates.find_elements_by_tag_name('li'):
        if val.text == time_period:
            val.click()
            break
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_gridCalendar_ctl00')))
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstBodies_Input').click()
    meetings = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstBodies_DropDown')
    for val in meetings.find_elements_by_tag_name('li'):
        if val.text == meeting_type:
            val.click()
            break
    WebDriverWait(driver, 10000).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_gridCalendar_ctl00')))    
    All_Meetings =  driver.find_element_by_id('ctl00_ContentPlaceHolder1_divGrid') 

    for element in All_Meetings.find_elements_by_link_text('Meeting details'): 
        link = element.get_attribute('href')
        if link is not None:
            get_agenda(link)
    driver.close()

def get_agenda(link):
    print(link)

    header_list = [ 'File #', 'Date', 'Meeting type', 'Staff Report link', 'Ver.', 'Agenda #', 'Agenda Note', 'Type', 'Title', 'Action', 'Result', 'Action Details', 'Video' ]
# this is a revised list of headers for the output csv file.

    tables = pd.read_html(link, keep_default_na=False)
    # sometimes generates ConnectionResetError

    meeting_name = tables[1].iloc[0,1].replace('/', '_')
# Grabbing meeting name from tables (for San Jose, tables[1] works, but need to make this dynamic for other cities with different table indexes)
    target_date = (tables[2].iloc[0,1]).split(' ')[0].replace('/', '-')
# Grabbing meeting date from tables (for San Jose, tables[2] works, but need to make this dynamic for other cities with different table indexes)
    last_table = len(tables) - 1
    agenda_table = tables[last_table].reindex(columns = header_list)
    agenda_table['Date'] = target_date
    agenda_table['Meeting type'] = meeting_name
# This adds new columns to dataframe for the 'Staff Report link', 'Date' and 'Meeting type'
    agenda_table = agenda_table[agenda_table['File #'] != '']
# Removes rows that don't have a File #
    l = agenda_table['File #'].tolist()
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

    agenda_table['Staff Report link'] = data
    agenda_table.to_csv((full_path + meeting_name + '_' + target_date + '.csv'), index=False, errors='replace')
# Creates filename with 'Meeting Name' and 'Date'
    drive_upload(full_path, drive)

scrape_meetings(current_city)
