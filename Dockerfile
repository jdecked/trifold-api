FROM python:3.6-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# and now all these env variables
ENV DJANGO_ENVIRONMENT production
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

# add and install requirements
RUN apk update && \
  apk add python3-dev mysql mysql-client mariadb-dev gcc musl-dev && \
  addgroup mysql mysql && \
  rm -rf /var/cache/apk/*
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r ./requirements.txt

# add app
ADD . /usr/src/app

EXPOSE 8000

# run server
ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["gunicorn", "-c", "./gunicorn.conf", "wsgi:application", "--log-file", "-"]
