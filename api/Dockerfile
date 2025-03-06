FROM python:3.11

RUN mkdir /login

WORKDIR /login

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
