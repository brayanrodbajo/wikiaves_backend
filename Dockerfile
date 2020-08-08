FROM python:3.7

EXPOSE 80
EXPOSE 443

WORKDIR /app

COPY requirements.txt /app/

COPY . /app/

RUN pip install daphne
RUN pip install -r requirements.txt

COPY wikiaves_backend/asgi.py /home/daphne/proj/
CMD daphne -b 0.0.0.0 -p 80 cpo.asgi:application
