# pull the official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /etc/opt/radak

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /etc/opt/radak
RUN pip install -r requirements.txt

# copy project
COPY . /etc/opt/radak
