FROM python:3.10.2
COPY . /app
WORKDIR /app
RUN pip install -r reqirements.txt
EXPOSE $PORT
CMD gunicorn --workers=4 --bind 0.0.0.0:PORT app:app