# Movie Analyzer - Working Python Reference

Architecture:

Browser -> NiceGUI frontend (:3000) -> FastAPI backend (:8000) -> Flask/TextBlob model (:5000)
                                                    -> PostgreSQL (:5432)

## Run with Docker

```bash
docker compose up --build
```

Open: http://localhost:3000

Useful endpoints:
- Backend Swagger: http://localhost:8000/docs
- Backend health: http://localhost:8000/health
- Model health: http://localhost:5000/health

Stop:

```bash
docker compose down
```

Reset the database:

```bash
docker compose down -v
docker compose up --build
```
