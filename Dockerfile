#FROM ubuntu:latest
#USER root
#RUN apt-get update -yqq && \
#    apt-get -yqq upgrade && \
#    apt-get install -yqq libpq-dev \
#    apt-get install gcc \
#    apt-get install -yqq python3.11 \
#    apt-get install -yqq python3-pip && \
#    apt-get clean

FROM python:3.11

WORKDIR /meme-bot

RUN  pip3 install --upgrade pip --no-cache-dir && \
     pip3 install --upgrade setuptools --no-cache-dir

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["python", "memebot.py"]