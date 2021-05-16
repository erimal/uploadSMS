#the base image
FROM python:3.8.2

# File author
MAINTAINER Eric Malm

ENV PYTHONUNBUFFERED 1

# Add project file to the user/src/app
ADD . /usr/src/app

# set directory to where to run command
WORKDIR /usr/src/app

# Copy the requirememt to the app folder 
COPY requirements.txt ./requirements.txt

RUN apt-get update && apt-get install -y  libldap2-dev libsasl2-dev ldap-utils

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

# Expose ports
EXPOSE 8091

#CMD [ "python3", "manage.py runserver 0.0.0.0:8000" ]
CMD [ "python3", "manage.py", "runserver","0.0.0.0:8091"]
