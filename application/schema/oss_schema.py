from pydantic import BaseModel, Field
from fastapi import Form, Query


class OssFileSchema(object):
    def __init__(self, name: str = Query(...), size: int = Query(...)):
        self.name = name
        self.size = size


class OssCallbackParamsSchema(BaseModel):
    name: str
    size: str

    class Config:
        orm_mode = True


class OssFileCallbackSchema(object):
    def __init__(self, name: str = Form(...), size: int = Form(...)):
        self.name = name
        self.size = size
