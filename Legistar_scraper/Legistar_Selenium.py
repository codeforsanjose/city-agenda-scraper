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

import glob
import os
import os.path
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from requests_html import HTMLSession

load_dotenv()
from get_agenda import get_agenda, master_list_creation
from GoogleDrive_upload import drive_upload, drive_launch

pdf_details = {}

def scrape_meetings(city_name="sanjose", time_period="Last Month", target_meeting="City Council"):
    def rename_file(new_name):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < 20:
            time.sleep(0.1)
            dl_wait = False
            for fname in os.listdir(full_path):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 0.1

        list_of_files = glob.glob(full_path + "/*")
        if len(list_of_files) > 0:
            latest_file = max(list_of_files, key=os.path.getmtime)
            os.rename(latest_file, full_path + '/' + new_name.replace('/', '-'))
            return True

        return False

    pdf_details['city_name'] = city_name

    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    prefs = {"download.default_directory": full_path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    actions = ActionChains(driver)

    session = HTMLSession()

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
    rows = target_range_table.find_elements_by_tag_name('tr') 
    Name_index = 0
    Meeting_Date_index = 1
    Meeting_Time_index = 2
    Meeting_Details_index = 4
    for row in rows[1:]: 
        cells = row.find_elements_by_tag_name('td')
        Name = cells[Name_index].text
        Meeting_Date = (cells[Meeting_Date_index].text).replace('/', '-')
        Meeting_Time = cells[Meeting_Time_index].text 
        try: 
            link = row.find_element_by_link_text('Meeting details').get_attribute('href')
        except: 
            continue
        if link is not None:
            get_agenda(link, Meeting_Date, Name, session)
#imported get_agenda function creates {meeting_name}_{meeting_date}.csv and append new rows to master_list.csv
#created csv files are added to {fullpath} dir
#==============================
            driver.execute_script(
                '''window.open("%s", "_blank");''' %link)
            WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
            driver.switch_to_window(driver.window_handles[1])
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located(
                (By.ID, 'ctl00_ContentPlaceHolder1_gridMain_ctl00')))

            pdf_details['meeting_name'] = driver.find_element_by_id(
                'ctl00_ContentPlaceHolder1_hypName').text
            pdf_details['meeting_date'] = driver.find_element_by_id(
                'ctl00_ContentPlaceHolder1_lblDate').text
            pdf_details['meeting_time'] = driver.find_element_by_id(
                'ctl00_ContentPlaceHolder1_lblTime').text

            meeting_rows = driver.find_element_by_id('ctl00_ContentPlaceHolder1_gridMain_ctl00').find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
            try:
                def get_a(el):
                    try:
                        return el.find_element_by_tag_name('td a')
                    except:
                        return None

                def get_href(el):
                    if el is not None:
                        return el.get_attribute('href')
                    else:
                        return None

                meeting_links = map(get_a, meeting_rows)
                agenda_links = filter(get_href, meeting_links)

                for agenda_link in agenda_links:
                    driver.execute_script(
                        '''window.open("%s", "_blank");''' %agenda_link.get_attribute('href'))
                    WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(3))
                    driver.switch_to_window(driver.window_handles[2])
                    pdf_details['file_number'] = driver.find_element_by_id(
                        'ctl00_ContentPlaceHolder1_lblFile2').text
                    pdf_details['version'] = driver.find_element_by_id(
                        'ctl00_ContentPlaceHolder1_lblVersion2').text
                    try:
                        # TODO change to link text contains 'memorandum'?
                        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Memorandum"))).click() 
                        memorandum = driver.find_element_by_link_text('Memorandum')
                        memorandum.click()
                        rename_file(pdf_details['city_name'] + '_'
                            + pdf_details['meeting_name'] + '_'
                            + pdf_details['meeting_date'] + '_'
#                            + pdf_details['meeting_time'] + '_'
                            + pdf_details['file_number'] + '_'
                            + pdf_details['version'] + '.pdf')
                    except Exception as error:
                        print(str(type(error)))
                        print(str(error.args))
                    finally:
                        driver.close()
                        driver.switch_to_window(driver.window_handles[1])
                        continue

            finally:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])

    driver.close()

if __name__ == "__main__":
    full_path = os.environ.get('full_path')

    current_city = sys.argv[1]
    time_period = sys.argv[2]
    target_meeting = sys.argv[3]

    if not os.path.exists(full_path + 'master_list.csv'):
        master_list_creation()

    scrape_meetings(current_city, time_period, target_meeting)
    drive = drive_launch()
    drive_upload(full_path, drive, sys.argv[1])

# https://docs.google.com/presentation/d/1_GfTIlF5si0LWDcsyWteF_rGwk2LaQJcXpSGxz0N5TY/edit?usp=sharing
