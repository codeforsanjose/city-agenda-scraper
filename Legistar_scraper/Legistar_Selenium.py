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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd

def scrape_meetings(city_name="sanjose", time_period="Last Month", target_meeting="City Council"):

    driver = webdriver.Chrome()
    actions = ActionChains(driver)

    driver.get("https://%s.legistar.com/Calendar.aspx" %city_name)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_tdYears')))

    driver.find_element_by_id('ctl00_ContentPlaceHolder1_tdYears').click()
    dates = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstYears_DropDown')
    for val in dates.find_elements_by_tag_name('li'):
        if val.text == time_period:
            val.click()
            break

    WebDriverWait(driver, 60).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_lstBodies_Input')))
# need to scroll element into view.

    meetings_dropdown = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstBodies_Input')
    actions.move_to_element(meetings_dropdown).perform()
    meetings_dropdown.click()
    menu_items = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lstBodies_DropDown')
    for item in menu_items.find_elements_by_tag_name('li'):
        if item.text == target_meeting:
            item.click()
            break

    WebDriverWait(driver, 60).until(EC.presence_of_element_located(
        (By.ID, 'ctl00_ContentPlaceHolder1_gridCalendar_ctl00')))

    target_range_table = driver.find_element_by_id('ctl00_ContentPlaceHolder1_gridCalendar_ctl00')
    for element in target_range_table.find_elements_by_link_text('Meeting details'):
        link = element.get_attribute('href')
        if link is not None:
            driver.execute_script(
                '''window.open("%s", "_blank");''' %link)
            WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
            driver.switch_to_window(driver.window_handles[1])
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located(
                (By.ID, 'ctl00_ContentPlaceHolder1_gridMain_ctl00')))

# NoSuchElementException when "No records to display" - convert to try-finally-continue?
            # agenda_links = filter(lambda el: el.get_attribute('href') is not None,
            #     map(lambda el: el.find_element_by_tag_name('td a'),
            #         driver.find_element_by_id('ctl00_ContentPlaceHolder1_gridMain_ctl00').find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')))

            meeting_rows = driver.find_element_by_id('ctl00_ContentPlaceHolder1_gridMain_ctl00').find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
            try:
                def get_a(el):
                    try:
                        return el.find_element_by_tag_name('td a')
                    except:
                        return None

                meeting_links = map(get_a, meeting_rows)
                def get_href(el):
                    if el is not None:
                        return el.get_attribute('href')
                    else:
                        return None

                agenda_links = filter(get_href, meeting_links)

                for agenda_link in agenda_links:
                    driver.execute_script(
                        '''window.open("%s", "_blank");''' %agenda_link.get_attribute('href'))
                    WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(3))
                    driver.switch_to_window(driver.window_handles[2])
                    try:
                        # TODO change to link text contains memorandum?
                        memorandum = driver.find_element_by_link_text('Memorandum')
                        memorandum.click()
                    finally:
                        driver.close()
                        driver.switch_to_window(driver.window_handles[1])
                        continue

            finally:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])

    driver.close()


def get_agenda(link):
    session = HTMLSession()

# this is a revised list of headers for the output csv file.
    header_list = [ 'File #', 'Staff Report link', 'Ver.', 'Agenda #', 'Agenda Note', 'Type', 'Title', 'Action', 'Result', 'Action Details', 'Video' ]
    tables = pd.read_html(link, keep_default_na=False)

# Grabbing meeting name from tables
    meeting_name = tables[2].iloc[0,1].replace('/', '_')
# Grabbing meeting date from tables
    target_date = (tables[3].iloc[0,1]).split(' ')[0].replace('/', '-')
    last_table = len(tables) - 1
# This adds a new column to dataframe for the 'Staff Report link'
    tables[last_table] = tables[last_table].reindex(columns = header_list)

# Grabs column of File # to find Staff Report hyperlinks
    l = tables[last_table]['File #'].tolist()
    data = []
# Loads Legistar 'Meeting Details' page
    r2 = session.get(link)

    for item in l:
# this checks for blank rows with no File # (Staff Report)
        if not item:
            data.append('')
        else:
# Finds hyperlinks from anchor tags
            report = r2.html.find('a', containing=str(item), first=True)
            try:
                data.append(report.attrs.get('href'))
            except:
                data.append('Error')
                continue

    tables[last_table]['Staff Report link'] = data
# Creates filename with 'Meeting Name' and 'Date'
    tables[last_table].to_csv((full_path + meeting_name + '_' + target_date + '.csv'), index=False, errors='replace')

if __name__ == "__main__":
    from dotenv import load_dotenv

    # if len(sys.argv) < 3:
    #     print("""To run this file properly, please include the following arguments:
    #         The city-name part of the Legistar URL.  i.e. https://<city name>.legistar.com.
    #         The desired time period.  It can be one of the following: All Years, Last Year, Last Month, Last Week, This Year, This Month, This Week, Today, Next Week, Next Month, Next Year.
    #     """)

    # else:

    load_dotenv()
    full_path = os.environ.get('full_path')
    current_city = sys.argv[1]
    time_period = sys.argv[2]
    target_meeting = sys.argv[3]

    scrape_meetings(current_city, time_period, target_meeting)
