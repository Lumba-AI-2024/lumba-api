FROM python:3.10

ENV PYTHONUNBUFFERED = 1

RUN mkdir /code
WORKDIR /code

COPY . .

COPY ./requirements.txt /requirements.txt

EXPOSE 8000

RUN pip install -r /requirements.txt
