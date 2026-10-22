# DevOps Capstone

[![CI Build](https://github.com/atharvkamthane/oaqjp-final-project-emb-ai/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/atharvkamthane/oaqjp-final-project-emb-ai/actions/workflows/ci-build.yaml)

A Flask-based **Account REST API Service** for the DevOps Capstone project. It demonstrates account CRUD operations, automated linting and testing, CORS support, HTTP security headers, and containerization.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m flask --app app run --host 0.0.0.0 --port 8080
```

The root endpoint returns:

```json
{"name":"Account REST API Service","version":"1.0"}
```

## Test and lint

```bash
nosetests --with-coverage --cover-package=app
flake8 app.py test_app.py
```

## API routes

- `GET /` — service metadata
- `POST /accounts` — create an account (`name`, `email`)
- `GET /accounts` — list accounts
- `GET /accounts/<id>` — read an account
- `PUT /accounts/<id>` — update an account
- `DELETE /accounts` — delete an account using JSON body `{"id":"<id>"}`
- `DELETE /accounts/<id>` — delete an account by ID

The badge shows the live GitHub Actions state for this repository. Do not consider the build successful unless the workflow run concludes successfully.
