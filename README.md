## Nuxt-Flask
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Nuxt](https://img.shields.io/badge/Nuxt-limegreen?style=flat&logo=nuxt&logoColor=white)](https://nuxt.com/)
[![Hono](https://img.shields.io/badge/Hono-orange?style=flat&logo=hono&logoColor=white)](https://hono.dev/)
[![Flask](https://img.shields.io/badge/Flask-darkcyan?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

Nuxt + Flask user auth application  
  
Nuxt: SPA + BFF (http://localhost:8080)
 - Lang, Syntax: TypeScript + Composition API (script setup)
 - CSS: Bootstrap
 - State management: Pinia
 - Unit test: Vitest
 - BFF: Hono
  
Flask: REST-API (http://localhost:8000)
 - Auth: JWT
 - ORM: SQLAlchemy
 - Validation: Pydantic
 - Unit test: Pytest
 - API docs: Swagger UI
 - Server: Gunicorn (gthread)

## How to Run
STEP1: Prepare .env files
```
# ./database.env
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"
POSTGRES_DB="db"

# ./backend.env
SQLALCHEMY_DATABASE_URI="postgresql+psycopg://user:password@database:5432/db"
JWT_SECRET_KEY="secret"

# ./frontend.env
API_URL_BASE="http://backend:8000"
FORCE_SSL_COOKIE="0"
```
STEP2: Run `$ docker compose up -d --build`
