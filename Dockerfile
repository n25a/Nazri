# pull the official base image
FROM python:3.8.9
# set work directory
WORKDIR /etc/opt/nazri

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN sudo pip install --upgrade pip
COPY requirements.txt /etc/opt/nazri/
RUN sudo pip install -r requirements.txt

# copy project
COPY . /etc/opt/nazri

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]