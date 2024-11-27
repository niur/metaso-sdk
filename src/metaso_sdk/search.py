import json
from httpx_sse import EventSource, connect_sse
from .client import client
from .model import Query, Topic

EventSource._check_content_type = lambda self: True


def search(query: Query, *, stream: bool = False, topic: Topic = None):
    if topic is not None:
        query.searchTopicId = topic.id

    if stream or query.stream:
        query.stream = True

    def _gen():
        with connect_sse(client, "POST", "/search/v2", json=query.model_dump()) as event_source:
            for sse in event_source.iter_sse():
                if (data := sse.data) != "[DONE]":
                    yield json.loads(data)

    if query.stream:
        return _gen()
    resp = client.post("/search/v2", json=query.model_dump())
    return resp.json()["data"]
