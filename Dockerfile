FROM python:3.6-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# and now all these env variables
ENV DATABASE_URL mysql://root@localhost/trifold_test
ENV DJANGO_ENVIRONMENT production
ENV DJANGO_SECRET_KEY ${DJANGO_SECRET_KEY}

# add and install requirements
RUN apk update && \
  apk add mysql mysql-client mariadb-dev gcc musl-dev && \
  addgroup mysql mysql && \
  rm -rf /var/cache/apk/*
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r ./requirements.txt
RUN python manage.py migrate

# add app
COPY . /usr/src/app

# run server
CMD ["gunicorn", "--certfile", "config/ssl/development/localhost-cert.pem", "--keyfile", "config/ssl/development/localhost-key.pem", "--ca-cert", "config/ssl/development/ca-cert.pem", "wsgi", "--log-file", "-"]
