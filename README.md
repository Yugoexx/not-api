# Not API

A note-taking REST API with user authentication, built with FastAPI, SQLAlchemy and SQLite.

## Features
- User registration and login with JWT tokens
- Passwords are hashed with Argon2 (never stored in plain text)
- Create, read, update and delete notes (CRUD)
- Every note belongs to a user; users can only access their own notes
- Request/response validation with Pydantic
- Automated tests with pytest (in-memory database)
- Interactive API docs at `/docs`

## Tech stack
Python, FastAPI, SQLAlchemy, SQLite, PyJWT, pytest

## Getting started

```bash
git clone https://github.com/Yugoexx/not-api.git
cd not-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "SECRET_KEY=$(openssl rand -hex 32)" > .env
fastapi dev main.py
```

Then open http://127.0.0.1:8000/docs

## Running tests

```bash
pytest -v
```

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/kayit` | No | Register a new user |
| POST | `/giris` | No | Log in and get a JWT token |
| GET | `/ben` | Yes | Get the current user |
| POST | `/notlar` | Yes | Create a note |
| GET | `/notlar` | Yes | List your notes |
| GET | `/notlar/{id}` | Yes | Get one note |
| PUT | `/notlar/{id}` | Yes | Update a note |
| DELETE | `/notlar/{id}` | Yes | Delete a note |

## Roadmap
- [x] CRUD endpoints
- [x] SQLite database with SQLAlchemy
- [x] User registration and login (JWT)
- [x] Notes belong to users
- [x] Tests
- [ ] Docker support
- [ ] Deployment