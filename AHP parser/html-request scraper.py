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

def granicus_check(site):

    error_words = [
    'government-website-design',
    'legistar',
    'granicusideas',
    'support.granicus',
    'digital-services-suite'
    ]
#added error_words to prevent false positives

#    if 'granicus' in site and not 'government-website-design' in site:
    if 'granicus' in site and not any(error_word in site for error_word in error_words):
        return True

#needs to prevent corporate granicus site links, 'www.granicus.com'


def legistar_check(site):
    if 'legistar' in site:
        return True

#sometimes pulls in pdfs, not the correct subdomain


session = HTMLSession()
i = 0
output_file = open('D:\\Github\\civic-scraper_Mark\\granicus_list2.csv', 'a+')
with open ('D:\Github\civic-scraper_Mark\\CA_city_websites_final.csv', encoding="utf-8") as csvfile:
    reader = csv.reader((x.replace('\0', '') for x in csvfile))
    for row in islice(reader, 0, None):
        Legistar = False
        Granicus = False
        data = []
        print('Im accessing: ' + row[2])

        try:
            response = session.get(row[2])
        except Exception as e:
                print("unsuccessful")
                data.append("unsuccessful")
                data.append(str(type(e)))
                data.append(str(e.args))
                data.append("\n")
                continue
        data.append(row[0])
        try:
            response.html.render(timeout=30)
        except Exception as e:
                print("unsuccessful")
                data.append("unsuccessful")
                data.append(str(type(e)))
                data.append(str(e.args))
                data.append("\n")
                continue

        anchors = response.html.find('a', containing='Agenda')
        link = 'None'
        for anchor in anchors:
            if 'AGENDA' in (anchor.text).upper():
                link = anchor.absolute_links
                break
            else:
                continue
        data.append(str(link))
#this new section tries to extract links with anchor text 'Agenda'
#should make this a loop for each link with Agenda so that it does the Granicus / Legistar search for a reliance score
#also need to strip out the '{}' from the html links

        sites = response.html.absolute_links


        for site in sites:
            if granicus_check(site):
                print('Granicus found')
                Granicus = True
                Granicus_site = site
                break
            if legistar_check(site):
                print('Legistar found')
                Legistar = True
                Legistar_site = site
                break
        data.append(str(Granicus))
        if Granicus:
            data.append(Granicus_site)
        else:
            data.append('None')
        data.append(str(Legistar))
        if Legistar:
            data.append(Legistar_site)
        else:
            data.append('None')
        data.append("\n")
        output_file.write(', '.join(data))
        output_file.flush()
        i += 1
        if i > 20:
            break
        print(Granicus, Legistar)

    output_file.close()
csvfile.close()