## Nuxt-Flask
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-blue.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

Nuxt + Flask user auth application  
  
Nuxt: SPA(Composition API & TS, CDN Bootstrap, Pinia state management, unit test)  
http://localhost:8080  
Flask: REST-API(JWT, CORS, ORM, schema validation, unit test, Swagger UI)  
http://localhost:8000  

## How to Run
STEP1: Prepare ./database.env & ./backend.env
```
# ./database.env
POSTGRES_USER="user"
POSTGRES_PASSWORD="password"
POSTGRES_DB="db"
```
```
# ./backend.env
SQLALCHEMY_DATABASE_URI="postgresql+psycopg://user:password@database:5432/db"
JWT_SECRET_KEY="secret"
```
STEP2: Run `$ docker compose up -d --build`
