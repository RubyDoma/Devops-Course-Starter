# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

Please follow these steps in order to run the project:
- Sing up to Trello or create an account
- Generate a Key
- Generate a Token
- Declare your Key and Token in the .env file


TESTING

There are 2 files containinig unit and integration tests:

test_app.py 
containing the unit tests created.
These tests will check that three lists (to do, doing, done) show their items only.

test_integration.py
containing the integration test created.
This tests checks that the API is working, and uses mocking to avoid making
external requests. It also doesn't have access to real
credentials.

To run the tests from a terminal (outside of any IDE) please use the following commands:

$ poetry run pytest 
or 
$ poetry run pytest todo_app/test_file_name.py

## ANSIBLE

Log to your Control Node and use this command to provision host VM:


$ ansible-playbook Playbook -i Inventory --ask-vault-pass

Make sure you can connect to your host VM via SSH for this command to run successfully.

## RUNNING APP LOCALLY IN A CONTAINER

Use the following command to spin up the three containers: dev, test and prod:

$ docker-compose up --build

Use the folliwing commands to spin up the three containers separately:

$ docker-compose up webapp-prod
$ docker-compose up webapp-dev
$ docker-compose up webapp-test

## OPEN APP IN HEROKU

https://todo-app-exercise-8.herokuapp.com/


