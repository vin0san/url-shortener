# nano-url-engine

A backend-focused URL shortener built to practice engineering decisions rather than maximize the number of technologies used.

The project implements URL shortening, authentication, ownership, click analytics, and a tested REST API while documenting the tradeoffs behind key design decisions.

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **Pydantic** — request/response validation
- **PyJWT** — JWT authentication
- **pwdlib (argon2)** — password hashing
- **pytest** — test suite (30 tests)

**Redis** isn't used — see [Design Decisions](#design-decisions).

## Architecture
```
                Client
                   │
            HTTP / JSON
                   │
             FastAPI Routes
                   │
        SQLAlchemy ORM
                   │
             PostgreSQL
```

## Project Structure

```bash
nano-url-engine/  
├── app/
│   ├── __init__.py
│   ├── main.py        
│   ├── config.py      
│   ├── database.py    
│   ├── models.py
│   ├── utils.py
│   ├── schemas.py
│   ├── routes.py
│   ├── auth.py
│   └── auth_routes.py      
├── database/
│   ├── schema.sql
│   ├── seeds.sql
│   └── queries.sql
├── tests/
│   ├── __init__.py
│   ├── conftest.py          
│   ├── test_shorten.py       
│   ├── test_health.py
│   ├── test_utils.py
│   ├── test_auth.py
│   ├── test_redirect.py
│   └── test_user.py          
├── requirements.txt
├── README.md               
└── .gitignore
```

## Features

- Shorten a URL, optionally with a custom key or an expiration window
- Redirect via short key, with correct HTTP semantics for missing (404) and expired (410) links
- Click tracking (user agent, referrer, timestamp) on every successful redirect
- Optional authentication — anyone can shorten a URL; logged-in users get their URLs tied to their account
- Ownership-scoped URL listing and per-URL click analytics (total clicks + daily breakdown)

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/shorten` | Optional | Create a short URL |
| GET | `/{short_key}` | None | Redirect to the original URL |
| POST | `/auth/register` | None | Create an account |
| POST | `/auth/login` | None | Get a JWT access token |
| GET | `/user/urls` | Required | List the authenticated user's URLs |
| GET | `/urls/{url_id}/analytics` | Required | Click analytics for a URL you own |

## Setup

**Prerequisites:** Python 3.12+, Docker (or local PostgreSQL 16+).

## Setup

**Prerequisites:** Python 3.12+, PostgreSQL 16+ (or Docker).

### Option A — Docker (recommended, no local Postgres needed)

```bash
git clone https://github.com/vin0san/nano-url-engine
cd nano-url-engine
cp .env.example .env
# fill in SECRET_KEY, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB in .env

docker compose up --build
```

App runs at `http://localhost:8000`, docs at `/docs`. Postgres schema initializes automatically on first run.

### Option B — Local Python + Postgres

```bash
git clone https://github.com/vin0san/nano-url-engine
cd nano-url-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill in DATABASE_URL, SECRET_KEY in .env

psql -U postgres -c "CREATE DATABASE url_production;"
psql -U postgres -d url_production -f database/schema.sql

uvicorn app.main:app --reload
```

Interactive API docs at `/docs` once it's running.

## Running Tests

```bash
# separate test database — keep this off the dev DB
psql -U postgres -c "CREATE DATABASE url_test;"
psql -U postgres -d url_test -f database/schema.sql

# add to .env
TEST_DATABASE_URL=postgresql://postgres:<password>@localhost:5432/url_test

pip install pytest httpx
pytest tests/ -v
```

30 tests covering utilities, health checks, URL creation, redirection, auth, and user-scoped endpoints.

## Design Decisions

**Click logging is synchronous.** At this project's actual traffic, effectively zero. A job queue or even `BackgroundTasks` would be infrastructure with nothing driving it. The click insert is wrapped in a broad `SQLAlchemyError` catch so a failed write can't block the redirect.

**`country_code` stays `NULL`.** Populating it needs a GeoIP lookup, which means a real external dependency. The column's there and nullable; the lookup isn't built because nothing's asking for it yet.

**Two different exception types on purpose.** `/shorten`'s collision retry catches `IntegrityError` specifically — the retry logic only makes sense if the failure actually was a key collision, so catching anything broader would mean retrying on unrelated DB errors too. Click-tracking catches the wider `SQLAlchemyError`, since any DB failure there gets the same treatment: log it if you can, never block the redirect.

**404, not 403, on someone else's URL analytics.** A 403 confirms the resource exists, that is an enumeration leak. 404 for both "doesn't exist" and "exists but isn't yours" gives nothing away.

**No automated test for concurrent key collisions.** The retry-on-`IntegrityError` path is implemented and reasoned through by hand, but a real concurrency test needs threading or mocking that's more than this project's actual traffic justifies. Noted here instead of left unexplained.

**No Redis.** Nothing in this project currently needs caching, rate limiting, or shared session state. Adding it without a real reason is the same mistake as adding it because it's "expected."

**pwdlib/argon2 instead of passlib/bcrypt.** Argon2's the more current default, and there's no legacy-hash migration to worry about here, which is the usual reason to reach for bcrypt instead. `pass_hash` is `VARCHAR(255)` rather than a fixed `CHAR`, since argon2 output length isn't guaranteed constant the way bcrypt's is.

**Login takes JSON, not an OAuth2 form.** FastAPI's `/docs` "Authorize" button expects the OAuth2 password-grant form convention, so it doesn't work here out of the box, this was a deliberate trade for staying consistent with the rest of the API, which is all JSON. Test tokens get passed manually via an `Authorization: Bearer` header instead.

## Future Work

- Redis cache-aside for redirect optimization
- Rate limiting
- Refresh token support
- GeoIP lookup
- CI/CD pipeline
- Structured logging