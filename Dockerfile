FROM python:3.10-slim

WORKDIR /app
COPY /requrements.txt .
RUN pip install -r requrements.txt
COPY . .

CMD python ./manage.py runserver 0.0.0.0:8000