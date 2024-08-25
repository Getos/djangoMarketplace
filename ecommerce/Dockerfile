FROM python:3.11-slim-bullseye


#env: show logs
ENV PYTHONUNBUFFERED=1
#UPDATE KERNAL + INSTALL DEP
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

#create  proj folder
WORKDIR /app

COPY requirements.txt /app/requirements.txt

#install req

RUN pip install -r /app/requirements.txt

#copy project code to docker

COPY . /app/