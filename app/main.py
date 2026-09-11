from fastapi import FastAPI

from app.routers.estimations import router as estimations_router

app = FastAPI(title="LLM Estimator", version="0.1.0")
app.include_router(estimations_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
