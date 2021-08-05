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

# TODO rename downloaded files according to convention.

import os
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def scrape_meetings(city_name="sanjose", time_period="Last Month", target_meeting="City Council"):

    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": full_path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
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


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    full_path = os.environ.get('full_path')
    current_city = sys.argv[1]
    time_period = sys.argv[2]
    target_meeting = sys.argv[3]

    scrape_meetings(current_city, time_period, target_meeting)
