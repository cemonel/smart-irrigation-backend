FROM python:3
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y gdal-bin
WORKDIR /smart_irrigation
COPY . .