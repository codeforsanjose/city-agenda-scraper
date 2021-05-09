#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      m_noa
#
# Created:     25/04/2021
# Copyright:   (c) m_noa 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(devtools=True)
    page = await browser.newPage()
    await page.goto('https://sanjose.legistar.com')
    dateSelector = await page.querySelector('#ctl00_ContentPlaceHolder1_tdYears')
    dates = await dateSelector.querySelectorAll('li')
    index = 0
    i = 0
    for date in dates:
        if await date.evaluate('el => el.textContent') == 'Last Week':
            index = i
        i += 1
    await dateSelector.click()
    await page.waitForSelector('#ctl00_ContentPlaceHolder1_lstYears_DropDown', visible=True )
    await dates[index].click()
    await page.waitForSelector('#ctl00_ContentPlaceHolder1_gridCalendar_ctl00')
    links = await page.querySelectorAll('#ctl00_ContentPlaceHolder1_gridCalendar_ctl00 a')
    for link in links:
        inText = await link.evaluate('el => el.textContent', force_expr=True)
        if inText == 'Agenda':
            link.click()
        print(link, inText)

    print('moo');
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())