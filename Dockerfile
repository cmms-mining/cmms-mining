FROM python:3.11
COPY requirements.txt /temp/requirements.txt
COPY source /source
COPY environment /environment
WORKDIR /source
RUN apt-get update -y
RUN apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt