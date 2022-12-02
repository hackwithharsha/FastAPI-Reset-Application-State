# pull official base image
FROM python:3.8.1-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install build-essential \
    && apt-get -y install libpq-dev \
    && apt-get -y install netcat gcc \
    && apt-get -y install python3-dev \
    && apt-get -y install python3-pip \
    && apt-get -y install unixodbc-dev \
    && apt-get -y install odbc-postgresql \
    && apt-get -y install python3-wheel \
    && apt-get -y install python3-setuptools \
    && apt-get clean

# install python dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install --upgrade wheel
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# EXPOSE 80

# CMD python -m app.main
