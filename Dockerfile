FROM python:3.7-alpine

RUN apk add --no-cache git

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
