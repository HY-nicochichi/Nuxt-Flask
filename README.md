## Nuxt-Flask
Nuxt + Flask user auth application  
Nuxt: SPA(Composition API & TS, CDN Bootstrap, Pinia state management)  
http://localhost:8080  
Flask: REST-API(JWT, CORS, ORM, validation, unit test, async server, Swagger UI)  
http://localhost:5000  
The command to just run the code: `docker compose up -d`  

## How to edit & run the code (Linux, Mac, Windows WSL)
Setup containers for edit
```shell
docker run -td --name python-dev python:3.14.2
docker run -td --name node-dev node:25.2.1
docker exec python-dev mkdir -p /Projects/Nuxt-Flask
docker exec node-dev mkdir -p /Projects/Nuxt-Flask
docker cp backend python-dev:/Projects/Nuxt-Flask
docker cp frontend node-dev:/Projects/Nuxt-Flask
```
Run the code edited
```shell
docker compose down -v --rmi local
rm -r backend frontend
docker cp python-dev:/Projects/Nuxt-Flask/backend .
docker cp node-dev:/Projects/Nuxt-Flask/frontend .
docker compose up -d
```
