FROM python:3.11.3-slim

RUN mkdir /src
WORKDIR /src
COPY . /src

RUN pip install -r requirements.txt