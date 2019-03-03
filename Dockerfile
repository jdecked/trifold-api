FROM python:3.6-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# and now all these env variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENVIRONMENT production
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ARG CLIENT_ID
ENV CLIENT_ID=${CLIENT_ID}
ARG HEROKU_POSTGRESQL_GREEN_URL
ENV HEROKU_POSTGRESQL_GREEN_URL=${HEROKU_POSTGRESQL_GREEN_URL}

RUN echo $HEROKU_POSTGRESQL_GREEN_URL

# add and install requirements
RUN apk update && \
  apk add python3-dev postgresql-dev gcc musl-dev && \
  rm -rf /var/cache/apk/*
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r ./requirements.txt

# add app
ADD . /usr/src/app

# run server
ENTRYPOINT [ "./entrypoint.sh" ]
CMD ["gunicorn", "-c", "./gunicorn.conf", "wsgi:application", "--log-file", "-"]
