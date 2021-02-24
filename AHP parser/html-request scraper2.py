#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Krammy
#
# Created:     13/01/2021
# Copyright:   (c) Krammy 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from requests_html import HTMLSession
import csv
from itertools import islice
from urllib.parse import urlparse

def error_check(error):
    data.append("unsuccessful")
    data.append(str(type(error)))
    data.append(str(error.args))
    data.append("\n")

def granicus_check(site):

    error_words = [
    'government-website-design',
    'legistar',
    'granicusideas',
    'support.granicus',
    'digital-services-suite'
    ]

    if 'granicus' in site and not any(error_word in site for error_word in error_words):
        u = urlparse(site)
        if u.path == '/ViewPublisher.php':
            return (u.scheme + '://' + u.netloc + u.path + '?' + u.query)
        else: return None
    else: return None

def legistar_check(site):

    u = urlparse(site)
    if u.path == '/Calendar.aspx' and (u.netloc).split('.')[0] != 'legistar':
        return (u.scheme + '://' + u.netloc + u.path)
    else: return None

#    Legistar site = 'https://alameda.legistar.com/Calendar.aspx'

def IQM2_check(site):

    u = urlparse(site)
    if u.path == '/Citizens/Detail_Meeting.aspx' or '/Citizens/default.aspx':
        return (u.scheme + '://' + u.netloc + u.path)
    else: return None


session = HTMLSession()
i = 0
output_file = open('D:\\Github\\civic-scraper_Mark\\granicus_list3.csv', 'a+')
with open ('D:\Github\civic-scraper_Mark\\CA_city_websites_final.csv', encoding="utf-8") as csvfile:
    reader = csv.reader((x.replace('\0', '') for x in csvfile))
    output_file.write(', '.join(['CITY', 'CITY_URL', 'LEGISTAR', 'IQM2', 'GRANICUS', '\n']))
    for row in islice(reader, 0, None):
        legistar = ''
        granicus = []
        IQM2 = ''
        data = []
        print('Im accessing: ' + row[0])
        try:
            response = session.get(row[2])
        except Exception as e:
            error_check(e)
            continue
        data.append(row[0])
        try:
            response.html.render(timeout=30)
        except Exception as e:
            error_check(e)
            continue
        sites = response.html.absolute_links
        for site in sites:
            if 'legistar' in site:
                legistar = legistar_check(site)
                if legistar != None:
                    break

            if 'iqm2' in site:
                IQM2 = IQM2_check(site)
                if IQM2 != None:
                    break

            if 'granicus' in site:
                if granicus_check(site) != None:
                    granicus.append(str(granicus_check(site)))

        data = [row[0], row[2], str(legistar), str(IQM2), '; '.join(granicus), '\n']
        output_file.write(', '.join(data))
        output_file.flush()
        i += 1
    output_file.close()
csvfile.close()

