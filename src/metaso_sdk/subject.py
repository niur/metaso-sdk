from pathlib import Path
from typing import Optional, List

from streamable import Stream

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
    return status.errCode == 0


def upload_file(topic: Topic, file) -> Optional[File]:
    resp = client.put(f"/file/{topic.dirRootId}", files={"file": file})
    json = resp.json()
    status = Status.model_validate(json)
    if status.errCode == 0:
        file = File.model_validate(json["data"][0])
        return file


def update_progress(file: File):
    resp = client.get(f"/file/{file.id}/progress")
    resp.raise_for_status()
    file.progress = resp.json()["data"]
    return file


def delete_file(file: File):
    resp = client.post("/file/trash", json={"ids": [file.id]})
    resp.raise_for_status()
    status = Status.model_validate(resp.json())
    return status.errCode == 0


def upload_directory(topic: Topic, path: Path, pattern="**/*", *, concurrency=10) -> List[File]:
    def _upload_file(file) -> File:
        with file.open("rb") as f:
            return upload_file(topic, f)

    files = list(
        Stream(Path(path).glob(pattern))
        .filter(Path.is_file)
        .map(_upload_file, concurrency=concurrency)
        .filter(lambda file: file is not None)
        .observe("files")
        .catch(finally_raise=True)
    )

    return files
