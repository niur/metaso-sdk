from .client import client
from .model import Query


def search(query: Query):
    resp = client.post("/search/v2", json=query.model_dump())
    resp.raise_for_status()
    return resp.json()["data"]
