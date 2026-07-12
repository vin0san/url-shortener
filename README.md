# URL Shortener

A production-inspired URL shortener built with FastAPI, PostgreSQL and Redis.

The goal of this project is to learn backend system design by implementing features commonly found in production services such as Bitly.

---

## Project Structure

```bash
nano-url-engine/  
├── app/
│   ├── __init__.py
│   ├── main.py        
│   ├── config.py      
│   ├── database.py    
│   └── models.py
│   └── utils.py      
├── database/
│   ├── schema.sql
│   ├── seeds.sql
│   └── queries.sql
├── .env               
└── .gitignore
```


## Planned Features

- Create short URLs
- Redirect service
- URL expiration
- Redis caching
- Click analytics
- User authentication
- Docker deployment
- Unit & integration tests

---

## Tech Stack

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Docker
- Pytest

---

## Current Progress

- [x] System architecture designed
- [x] Database schema
- [x] SQL queries
- [x] Seed data
- [ ] API implementation
- [ ] Redis cache
- [ ] Analytics pipeline
- [ ] Docker
- [ ] Tests