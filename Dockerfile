FROM python:3.6-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# and now all these env variables
ENV DJANGO_ENVIRONMENT production

# add and install requirements
RUN apk update && \
  apk add mysql mysql-client mariadb-dev gcc musl-dev && \
  addgroup mysql mysql && \
  rm -rf /var/cache/apk/*
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r ./requirements.txt

# add app
COPY . /usr/src/app
RUN python ./manage.py migrate

# run server
CMD ["gunicorn", "--certfile", "config/ssl/development/localhost-cert.pem", "--keyfile", "config/ssl/development/localhost-key.pem", "--ca-cert", "config/ssl/development/ca-cert.pem", "wsgi", "--log-file", "-"]
