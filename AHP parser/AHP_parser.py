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
import requests
import csv
from itertools import islice
from urllib.parse import urlparse

def error_check(error):
    data.append("unsuccessful")
    data.append(str(type(error)))
    data.append(str(error.args))
    data.append("\n")

def novusagenda_check(site):

    paths = [
    '/agendapublic/',
    'MeetingsGeneral.aspx'
    ]

    u = urlparse(site)
    if any(path.upper() in (u.path).upper() for path in paths):
        return (u.scheme + '://' + u.netloc + u.path)
    else: return None

# PLACE.novusagenda.com/agendapublic

def primegov_check(site):

    u = urlparse(site)
    if (    u.path.upper() == 'primegov.com/public/portal/'.upper()
            and requests.get(u.scheme + '://' + u.netloc + u.path + 'search').status_code == 200):
        return (u.scheme + '://' + u.netloc + u.path)
    else: return None

# not working yet .... line 43 u.path needs to only bring /portal, not /portal/meeting/\
# PLACE.primegov.com/public/portal/search

def IQM2_check(site):

    u = urlparse(site)
    if u.path == '/Citizens/Detail_Meeting.aspx' or '/Citizens/default.aspx':
        return (u.scheme + '://' + u.netloc + u.path)
    else: return None

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




session = HTMLSession()
i = 0

output_file = open('D:\\Github\\civic-scraper_Mark\\granicus_list4.csv', 'a+')
with open ('D:\Github\civic-scraper_Mark\\CA_city_websites_final.csv', encoding="utf-8") as csvfile:
    reader = csv.reader((x.replace('\0', '') for x in csvfile))

    output_file.write(', '.join([
    'CITY',
    'CITY_URL',
    'LEGISTAR',
    'IQM2',
    'NOVUSAGENDA',
    'PRIMEGOV',
    'GRANICUS',
    '\n'
    ]))

    for row in islice(reader, 0, None):
        legistar = ''
        granicus = []
        IQM2 = ''
        novus = ''
        primegov = ''
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
        except Exception as error:
            print(str(type(error)))
            print(str(error.args))
            continue
        sites = response.html.absolute_links
        for site in sites:
            if 'legistar' in site:
                legistar = legistar_check(site)
                if legistar != None:
                    break

            if 'novus' in site:
                novus = novusagenda_check(site)
                if novus != None:
                    break

            if 'primegov' in site:
                primegov = primegov_check(site)
                if primegov != None:
                    break

            if 'iqm2' in site:
                IQM2 = IQM2_check(site)
                if IQM2 != None:
                    break

            if 'granicus' in site:
                if granicus_check(site) != None:
                    granicus.append(str(granicus_check(site)))

        data = [
        row[0],
        row[2],
        str(legistar),
        str(IQM2),
        str(novus),
        str(primegov),
        '; '.join(granicus),
        '\n'
        ]
        output_file.write(', '.join(data))
        output_file.flush()
        i += 1
    output_file.close()
csvfile.close()

