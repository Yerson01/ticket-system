FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .temp-deps \
    gcc libc-dev linux-headers libffi-dev musl-dev \
    openssl-dev cargo postgresql-dev

RUN mkdir /ticket-system
WORKDIR /ticket-system
COPY ./requirements /requirements
RUN pip3 install --upgrade pip && \
    pip3 install -r /requirements/dev.txt

COPY . /ticket-system/
