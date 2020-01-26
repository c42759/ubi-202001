FROM python:2.7.17-alpine
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir /code
WORKDIR /code

