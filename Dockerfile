# syntax=docker/dockerfile:1
FROM selenium/standalone-chrome

WORKDIR /selenium-docker

COPY requirements.txt requirements.txt

USER root

RUN apt-get update \
    && apt-get install python3-distutils -y \
    && apt-get install python3-pip

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
# RUN pip3 install -r requirements.txt
RUN python3 -m pip3 install selenium
COPY . .
# CMD python3 /selenium-docker/Legistar_Selenium.py
CMD [ "python3", "-m" , "Legistar_Selenium", "run", "--host=0.0.0.0:8080"]