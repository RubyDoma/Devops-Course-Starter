FROM python:3.9.7-slim-buster as base
RUN apt-get update
COPY . /opt/
WORKDIR /opt
RUN pip install -r requirements.txt

FROM base as production
EXPOSE 80
ENTRYPOINT ["/opt/gunicorn.sh"]

FROM base as development
EXPOSE 5000
ENTRYPOINT [ "/opt/flask.sh" ]

FROM base as test
ENTRYPOINT [ "/opt/test.sh" ]