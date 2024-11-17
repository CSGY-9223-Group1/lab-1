# syntax=docker/dockerfile:1

FROM python:3.8-alpine

WORKDIR /lab-1

COPY . /lab-1

RUN python -m pip install pipenv
RUN pipenv install

EXPOSE 5000

CMD ["pipenv", "run", "python3", "main.py"]