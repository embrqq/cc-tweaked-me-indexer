from fastapi import APIRouter

metrics = APIRouter(prefix="/metrics")


@metrics.get("/")
def get_metrics():
    return {"msg": "Hello World!"}
