#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krammy
#
# Created:     25/02/2021
# Copyright:   (c) Krammy 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas as pd
from requests_html import HTMLSession


def get_meetings(url):
    links = []
    r = session.get(url)
    r.html.render()
    meetings = r.html.find('a', containing='details')
# grabs meetings based off 'details' as anchor text
    for meeting in meetings:
        link = meeting.attrs.get('href')
        if link is not None:
            links.append(link)

    for item in links:
        get_agenda(item)

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

    tables = pd.read_html((url[:-13] + link), keep_default_na=False)

    Meeting_name = tables[2].iloc[0,1]
# Grabbing meeting name from tables
    Date = (tables[3].iloc[0,1]).split(' ')[0].replace('/', '-')
# Grabbing meeting date from tables
    tables[11] = tables[11].reindex(columns = header_list)
# This adds a new column to dataframe for the 'Staff Report link'

    l = tables[11]['File #'].tolist()
# Grabs column of File # to find Staff Report hyperlinks
    data = []
    r2 = session.get(url[:-13] + link)
# Loads Legistar 'Meeting Details' page (the [:-13] removes the 'Calendar.aspx')
    for item in l:
        if not item:
            data.append('')
        else:
            report = r2.html.find('a', containing=str(item), first=True)
# Finds hyperlinks from anchor tags
            try: data.append(report.attrs.get('href'))
            except:
                data.append('Error')
                continue

    tables[11]['Staff Report link'] = data
    tables[11].to_csv((path + Meeting_name + ' ' + Date + '.csv'), index=False, errors='replace')
# Creates filename with 'Meeting Name' and 'Date'


path = 'D:\\Github\\city-agenda-scraper\\agenda_tables\\'
#this is the path from where meeting.csv files should go
url = 'https://sanjose.legistar.com/Calendar.aspx'
# test url for now, later will be list of urls to loop thru
session = HTMLSession()

get_meetings(url)