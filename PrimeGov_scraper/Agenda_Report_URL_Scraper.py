import pandas as pd
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
city = 'san-mateo'  # change this to match the .csv file with the city agenda urls to be polled
path_to_data = './data/'
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options) # Make sure you have the correct driver
city_df = pd.read_csv(path_to_data + city + '.csv', header=0)
agenda_df = city_df[city_df['doc_type'] == 'Agenda']
agenda_report_df = pd.DataFrame(columns=['url'])

for agenda in agenda_df.url.values:
    driver.get(agenda)
    all_elements = driver.find_elements_by_xpath("//a[contains(@title,'Download Agenda Report')]")
    for elem in all_elements:
        agenda_report_df = agenda_report_df.append({'url': elem.get_attribute("href")}, ignore_index=True)
    print(f'Scraping Agenda {agenda} found {len(all_elements)} Agenda Reports')
print(f'Total: {agenda_report_df.shape[0] - 1} Reports Found')
agenda_report_df.to_csv(path_to_data + city + '_agenda_report_urls.csv')
print(f'{path_to_data}{city}_agenda_report_urls.csv Saved')
