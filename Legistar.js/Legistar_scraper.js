const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({devtools: true});
  const page = await browser.newPage();
  await page.goto('https://sanjose.legistar.com');
  // const menu = await page.$('.rtsUL');
  // const items = await menu.$$('li');
  // await items[1].click();
  // await page.waitForSelector('#ctl00_ContentPlaceHolder1_tdYears');
  const dateSelector = await page.$('#ctl00_ContentPlaceHolder1_tdYears');
  const dates = await dateSelector.$$('li');
  let index;
  for (let i = 0; i < dates.length; i += 1) {
    if (await dates[i].evaluate(el => el.textContent) === 'Last Week') {
      index = i;
    }
  }
  await dateSelector.click();
  await page.waitForSelector('#ctl00_ContentPlaceHolder1_lstYears_DropDown', { visible: true })
  await dates[index].click();
  await page.waitForSelector('#ctl00_ContentPlaceHolder1_gridCalendar_ctl00');
  const links = await page.$$('#ctl00_ContentPlaceHolder1_gridCalendar_ctl00 a');

  for (let i = 0; i < links.length; i += 1) {
    const inText = await links[i].evaluate(el => el.textContent);
    if (inText === 'Agenda') {
      links[i].click();
      console.log(i, inText);
    }
  }

  console.log('moo');

  await browser.close();
})();
