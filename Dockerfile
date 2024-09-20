# syntax=docker/dockerfile:1

FROM python:3.8-alpine

WORKDIR /lab-1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /lab-1

EXPOSE 5000

CMD ["python3", "main.py"]