FROM python:3.10.3-slim-buster as base
RUN apt-get update
COPY . /opt/
WORKDIR /opt
RUN pip install poetry
RUN poetry config virtualenvs.create false --local && poetry install

FROM base as development
EXPOSE 5000
ENTRYPOINT ["sh", "/opt/flask.sh" ]

FROM base as test
ENV PATH="${PATH}:/root/todo_app"
CMD ["poetry", "run", "pytest"]

FROM base as production
EXPOSE 80
RUN chmod +x /opt/gunicorn.sh
CMD poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:$PORT
#The CD pipeline assumes that the production container is the last target
