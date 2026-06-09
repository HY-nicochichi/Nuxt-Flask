## Nuxt-Flask
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Nuxt](https://img.shields.io/badge/Nuxt-mediumseagreen?style=flat&logo=nuxt&logoColor=white)](https://nuxt.com/)
[![Hono](https://img.shields.io/badge/Hono-orange?style=flat&logo=hono&logoColor=white)](https://hono.dev/)
[![Flask](https://img.shields.io/badge/Flask-darkcyan?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

Nuxt + Flask user auth application  

Nuxt: SPA + BFF (http://localhost:8080)
 - Lang, Syntax: TypeScript + Composition API (script setup)
 - CSS: Bootstrap
 - State management: Pinia
 - Unit test: Vitest
 - BFF: Hono

Flask: REST API (http://localhost:8000)
 - Auth: JWT
 - ORM: SQLAlchemy
 - Validation: Pydantic
 - Unit test: Pytest
 - Type check: Pyright
 - API docs: Swagger UI
 - Server: Gunicorn (gthread)

### How to run
```bash
docker compose up -d
```
