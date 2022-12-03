# Boilerplate for Flask using postgres database

Originally forked from [this](https://github.com/3sarojbhattarai/flask-postgres-api-bp) repo. Reworked, improved and added my preferences to it.

## Installation
Run the following commands to set up the project:
```bash
cp .env.example .env
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Install the dev dependencies:
```bash
pip install -r dev-requirements.txt
```
Or just install all the dependencies:
```bash
pip install -r all-requirements.txt
```

### If you are not using a .env file
If you are not using a .env file, you need to set up the environment variables below. The example below is the defaults (no need to set them if you are using the default values):
```bash
export ENV=dev
export FLASK_APP=main
```
And if you are using a postgres database, you need to set up the environment variables below. The example below is the defaults (no need to set them if you are using the default values):
```bash
export DB_DIALECT=postgresql
export DB_HOST=127.0.0.1
export DB_PORT=5432
export DB_NAME=blank
export DB_USERNAME=postgres
export DB_PASSWORD=
```