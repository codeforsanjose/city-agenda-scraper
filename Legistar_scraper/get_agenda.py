import pandas as pd
from requests_html import HTMLSession
import os
from os.path import exists
import csv

header_list = [ 'File #', 'Date', 'Meeting type', 'Staff Report link', 'Ver.', 'Agenda #', 'Agenda Note', 'Type', 'Title', 'Action', 'Result', 'Action Details', 'Video' ]


full_path = os.environ.get('full_path')
def get_agenda(link, meeting_date, meeting_name):
    master_list_creation()
    session = HTMLSession()
    print(link)

#    header_list = [ 'File #', 'Date', 'Meeting type', 'Staff Report link', 'Ver.', 'Agenda #', 'Agenda Note', 'Type', 'Title', 'Action', 'Result', 'Action Details', 'Video' ]
# this is a revised list of headers for the output csv file, more may be added later

    tables = pd.read_html(link, keep_default_na=False)
    last_table = len(tables) - 1
    agenda_table = tables[last_table].reindex(columns = header_list)
    agenda_table['Date'] = meeting_date
    agenda_table['Meeting type'] = meeting_name
# This adds new columns to dataframe for the 'Staff Report link', 'Date' and 'Meeting type'
    agenda_table = agenda_table[agenda_table['File #'] != '']
# Removes rows that don't have a File #, these are typically procedural agenda items with no staff report
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
    master_list(agenda_table)

def master_list_creation(): 
    if not exists(full_path + 'master_list.csv'): 
        with open(full_path + 'master_list.csv', 'w+', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header_list)
        csvfile.close()

def master_list(df):
    #need to add in check for full_path + master_list, add in headers if new) 
    #if not exists(full_path + 'master_list.csv'): 
    #    with open(full_path + 'master_list.csv', 'w+') as csvfile:
    #        writer = csv.writer(csvfile)
    #        writer.writerow(header_list)
    #    csvfile.close()
    caller = pd.read_csv(full_path + 'master_list.csv', encoding='utf-8')
    caller = caller.append(df, ignore_index=False)
    caller = caller.drop_duplicates(subset=['Date', 'Meeting type', 'Agenda #'], )
    caller.to_csv(full_path + 'master_list.csv', index=False)

#    master_list(agenda_table) 
# Creates filename with 'Meeting Name' and 'Date'
#    drive_upload(full_path, drive)

#get_agenda('https://sanjose.legistar.com/MeetingDetail.aspx?ID=890211&GUID=3AA3C6A1-20A0-49CD-8E39-AA095DEC160A&Options=info|&Search=', '10-05-2021', 'sanjose')