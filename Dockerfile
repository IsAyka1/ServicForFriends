FROM python:3.8
ENV PYTHONUNBUFFERED 1  # no buffer

ADD server_for_friends /service
RUN mkdir /service/static
RUN mkdir /service/media
WORKDIR /service

RUN pip install -r requirements.txt
