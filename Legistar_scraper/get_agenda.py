import csv
import os
from os.path import exists

import pandas as pd
from requests_html import HTMLSession

header_list = ['File #', 'Date', 'Meeting type', 'Staff Report link', 'Ver.', 'Agenda #', 'Agenda Note', 'Type',
               'Title', 'Action', 'Result', 'Action Details', 'Video']
full_path = os.environ.get('full_path')


def get_agenda(link, meeting_date, meeting_name, session):
    print(link)
    agenda_table = find_agenda_table(link).reindex(columns=header_list)
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


def find_agenda_table(link):
    tables = pd.read_html(link, keep_default_na=False)
    last_table = len(tables) - 1
    table = tables[last_table]
    return table


def master_list_creation():
    with open(full_path + 'master_list.csv', 'w+', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header_list)
    csvfile.close()


def master_list(df):
    caller = pd.read_csv(full_path + 'master_list.csv', encoding='utf-8')
    caller = caller.append(df, ignore_index=False)
    caller = caller.drop_duplicates(subset=['Date', 'Meeting type', 'Agenda #'], )
    caller.to_csv(full_path + 'master_list.csv', index=False)
