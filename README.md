# city-agenda-scraper

Code for San Jose's Agenda Scraper is an open-source tool to parse through publicly available agendas and staff reports to provide a centralized repository of local government actions. Our goal is help community members learn about what their local government is actively discussing and focusing on. \

'Wait a second,' you might be thinking. 'Aren't all government meetings and agendas already posted to local city websites?' \
You're absolutely correct! Cities do a good job following the letter of the law in publishing all required documents to their websites. But the problem is they don't necessarily follow the spirit of the law. Local government documents are quite boring and hard to parse, and there's a lack of effort to boil down complex issues for the public to understand. \

Scraping the city's document archives is a first step for us to work on analyzing these documents and provide better public notification.  

At this point, the primary scraper we are refining is for Legistar, which is the hosting platform used by San Jose and many other cities across California. You can find this scraper script and its associated files in the repo’s city-agenda-scraper/Legistar_scraper folder. 

## running the scraper

To run the Legistar scraper, you will need to first set up two files in your local /Legistar_scraper repository: 

- .env file 

- launch.json

### .env 

The .env file declares environment variables on your local drive. It is essentially a text file, but make sure it has a .env extension, not a .txt extension. The variables you need to declare include: 

`full_path = ‘{path-where-I-want-files-to-go}’`

### launch.json 

The launch file sets the arguments that will be called by the scraper for different cities that we scrape. You can set this up in most IDE environments as a run configuration. The arguments that are needed by the script include: 

`arg[0] : {city name as used in Legistar url path}` 

For example, San Jose’s legistar page is https://sanjose.legistar.com. The url string we need here is “sanjose” 

`arg[1]` : Time range to scrape. The default we’re using is “This Month” 

`arg[2]` : The government body to scrape. The default we’re using is “City Council” 

Example launch.json: 

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Legistar - San Jose",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "cwd": "${fileDirname}/",
            "console": "integratedTerminal",
            "args": ["sanjose", "This Month", "City Council"]
        }
    ]

}
```
