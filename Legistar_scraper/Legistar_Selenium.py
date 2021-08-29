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

full_path = os.environ.get('full_path')
drive = drive_launch()
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
    rows = All_Meetings.find_elements_by_tag_name('tr') 
    Name_index = 0
    Meeting_Date_index = 1
    Meeting_Time_index = 2
    Meeting_Details_index = 4
    i = 0
    for header in rows[0].find_elements_by_tag_name('th'):
        if header.text == "Name":   
            Name_index = i
            print('Name found')
        if header.text == "Meeting Date ":
            Meeting_Date_index = i
            print('MD found')
        if header.text == "Meeting Time": 
            Meeting_Time_index = i
            print('MT')
        if header.text == "Meeting Details": 
            Meeting_Details_index = i
            print('MDetails')
        i += 1
    for row in rows[1:]: 
        cells = row.find_elements_by_tag_name('td')
        Name = cells[Name_index].text
        Meeting_Date = (cells[Meeting_Date_index].text).replace('/', '-')
        Meeting_Time = cells[Meeting_Time_index].text
        link = cells[Meeting_Details_index].find_element_by_link_text('Meeting details').get_attribute('href')

        if link is not None:
   
   
            get_agenda(link, Meeting_Date, Name)
    driver.close()

def get_agenda(link, meeting_date, meeting_name):
    print(link)

    header_list = [ 'File #', 'Date', 'Meeting type', 'Staff Report link', 'Ver.', 'Agenda #', 'Agenda Note', 'Type', 'Title', 'Action', 'Result', 'Action Details', 'Video' ]
# this is a revised list of headers for the output csv file.

    tables = pd.read_html(link, keep_default_na=False)
    # sometimes generates ConnectionResetError

    last_table = len(tables) - 1
    agenda_table = tables[last_table].reindex(columns = header_list)
    agenda_table['Date'] = meeting_date
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
    agenda_table.to_csv((full_path + meeting_name + '_' + meeting_date + '.csv'), index=False, errors='replace')
# Creates filename with 'Meeting Name' and 'Date'
    drive_upload(full_path, drive)

scrape_meetings(current_city)
