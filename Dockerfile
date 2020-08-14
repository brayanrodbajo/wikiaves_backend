FROM python:3-alpine
ADD . /api
WORKDIR /api
# You will need this if you need PostgreSQL, otherwise just skip this
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN pip install -r requirements.txt
# Installing uwsgi server
RUN pip install uwsgi
EXPOSE 8000
# This is not the best way to DO, SEE BELOW!!
CMD uwsgi --http "0.0.0.0:8000" --module api.wsgi --master --processes 4 --threads 2