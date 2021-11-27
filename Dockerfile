FROM python:3.9

WORKDIR .

RUN pip install --upgrade pip && pip install pipenv

RUN apt-get -q update && apt-get -qy install netcat

COPY . .

RUN pipenv install --system --deploy

EXPOSE 8000
