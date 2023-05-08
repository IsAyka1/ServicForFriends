FROM python:3.8
ENV PYTHONUNBUFFERED 1  # no buffer
# RUN pip install pipenv && pipenv install
ADD server_for_friends /service
WORKDIR /service
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
