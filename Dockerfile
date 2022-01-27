# syntax=docker/dockerfile:1
FROM selenium/standalone-chrome

WORKDIR /selenium-docker

COPY requirements.txt requirements.txt

USER root

RUN apt-get update
RUN apt-get install python3-distutils -y
RUN apt-get install python3-pip -y

RUN pip3 install -r requirements.txt

RUN mkdir data
COPY Legistar_scraper ./Legistar_scraper

CMD python3 /selenium-docker/Legistar_scraper/Legistar_Selenium.py sanjose "This Month" "City Council"
