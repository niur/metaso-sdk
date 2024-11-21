from .client import client
from .model import Status, Topic, File


def create_topic(topic: Topic):
    resp = client.put("/topic", json=topic.model_dump())
    resp.raise_for_status()
    topic = Topic.model_validate(resp.json()["data"])
    return topic


def delete_topic(topic: Topic) -> bool:
    resp = client.post("/topic/trash", json={"ids": [topic.id]})
    resp.raise_for_status()
    status = Status.model_validate(resp.json())
    return status.code == 0


def upload_file(topic: Topic, file):
    resp = client.put(f"/file/{topic.dir_root_id}", files={"file": file})
    resp.raise_for_status()
    file = File.model_validate(resp.json()["data"][0])
    return file


def get_progress(file: File):
    resp = client.get(f"/file/{file.id}/progress")
    resp.raise_for_status()
    return resp.json()["data"]


def delete_file(file: File):
    resp = client.post("/file/trash", json={"ids": [file.id]})
    resp.raise_for_status()
    status = Status.model_validate(resp.json())
    return status.code == 0
