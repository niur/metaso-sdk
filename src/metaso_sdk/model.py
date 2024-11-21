from typing import Optional
from pydantic import BaseModel, Field


class Status(BaseModel):
    code: int = Field(alias="errCode")
    message: str = Field(alias="errMsg")


class Topic(BaseModel):
    id: Optional[str]
    name: str
    dir_root_id: Optional[str] = Field(alias="dirRootId")
    description: Optional[str]


class File(BaseModel):
    id: Optional[str]
    name: str = Field(alias="fileName")
    parent_id: str = Field(alias="parentId")
    type: str = Field(alias="contentType")
    size: int
    preview_url: Optional[str] = Field(alias="previewUrl", default="")
    original_url: Optional[str] = Field(alias="originalUrl")
    progress: int
