# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install pipenv
COPY . /code
WORKDIR /code/
RUN pipenv install --system

EXPOSE 8000

# Setup GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal

# set work directory
WORKDIR /code/
# Add wait-for-it
#COPY wait-for-it.sh wait-for-it.sh
#RUN ["chmod", "+x", "wait-for-it.sh"]
#
#ENTRYPOINT [ "/bin/bash", "-c" ]
#CMD ["./wait-for-it.sh" , "postgis:5432" , "--strict" , "--timeout=300" , "--" , "python", "manage.py", "migrate", "--no-input"]

CMD ["python", "manage.py", "migrate", "--no-input"]