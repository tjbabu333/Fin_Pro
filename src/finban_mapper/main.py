"""FastAPI app entrypoint."""

from fastapi import FastAPI

from finban_mapper.api.routes import router as entities_router

app = FastAPI(title="finban mapping service")
app.include_router(entities_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
