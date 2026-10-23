# Not API

A simple note-taking REST API built with FastAPI, SQLAlchemy and SQLite.

## Features
- Create, read, update and delete notes (CRUD)
- Data persisted in a SQLite database
- Request/response validation with Pydantic
- Interactive API docs at `/docs`

## Tech stack
Python, FastAPI, SQLAlchemy, SQLite

## Getting started

```bash
git clone https://github.com/Yugoexx/not-api.git
cd not-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

Then open http://127.0.0.1:8000/docs

## Roadmap
- [ ] User registration and login (JWT)
- [ ] Notes belong to users
- [ ] Tests