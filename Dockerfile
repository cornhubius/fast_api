FROM python:3.9

WORKDIR .

RUN pip install --upgrade pip && pip install pipenv && \
    apt-get -q update && apt-get -qy install netcat

COPY . .

RUN curl -OL https://raw.githubusercontent.com/mrako/wait-for/master/wait-for && chmod +x wait-for && \
    pipenv install --system --deploy

EXPOSE 8000