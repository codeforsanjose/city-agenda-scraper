import pandas as pd
from selenium import webdriver
import subprocess
import re

options = webdriver.ChromeOptions()
options.add_argument("--headless")
city = 'san-mateo'  # change this to match the .csv file with the city agenda urls to be polled
path_to_data = './data/'
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options) # Make sure you have the correct driver
city_df = pd.read_csv(path_to_data + city + '.csv', header=0)
agenda_df = city_df[city_df['doc_type'] == 'Agenda']
agenda_report_df = pd.DataFrame(columns=['url'])

for index, agenda in agenda_df.iterrows():
    driver.get(agenda['url'])
    all_elements = driver.find_elements_by_xpath("//a[contains(@title,'Download Agenda Report')]")
    for elem in all_elements:
        # Grab the Agenda Report url
        agenda_report_df = agenda_report_df.append({'url': elem.get_attribute("href")}, ignore_index=True)
        # Create download filename from original dataframe plus document id
        download_file = \
            agenda['city'].replace(' ', '_') + '_' + agenda['meeting'].replace(' ', '_') + '_' + agenda['date'][:10] + \
            '_' + re.findall(r'\d+', elem.get_attribute('pathname'))[0] + '.pdf'
        # Save pdf to local disk
        subprocess.run(["powershell", "Invoke-WebRequest " + {'url': elem.get_attribute("href")}.get('url') +
                        " -OutFile " + "'" + path_to_data + download_file + "'"])
    print(f'Scraping Agenda {agenda["city"]} {agenda["meeting"]} found {len(all_elements)} Agenda Reports')
print(f'Total: {agenda_report_df.shape[0] } Reports downloaded')
agenda_report_df.to_csv(path_to_data + city + '_agenda_report_urls.csv')
print(f'{path_to_data}{city}_agenda_report_urls.csv Saved')
