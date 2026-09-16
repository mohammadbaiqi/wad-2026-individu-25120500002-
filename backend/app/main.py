from fastapi import FastAPI

from app import routers

app = FastAPI(title="WAD 2026 - Individu API")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(routers.router)