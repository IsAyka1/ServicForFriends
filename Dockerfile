FROM python:3.8
ENV PYTHONUNBUFFERED 1  # no buffer

ADD server_for_friends /service
WORKDIR /service

RUN pip install -r requirements.txt
RUN adduser --disabled-password --no-create-home docuser
USER docuser
