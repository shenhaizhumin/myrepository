from pydantic import BaseModel, Field
from datetime import datetime


class UmsMenuSchema(BaseModel):
    # id = Field(..., Integer, primary_key=True, nullable=False)
    parent_id: int = Field(..., alias='parentId', nullable=False, description='父级ID')
    title: str = Field(..., nullable=False, description='菜单名称')
    name: str = Field(..., nullable=False, description='前端名称')
    icon: str = Field(..., nullable=False, description='前端图标')
    level: int = Field(..., nullable=False, description='菜单级数')
    hidden: int = Field(..., nullable=False, description='前端隐藏')
    sort: int = Field(..., nullable=False, description='菜单排序')


class UmsMenuUpdateSchema(BaseModel):
    # id = Field(..., Integer, primary_key=True, nullable=False)
    parent_id: int = Field(None, alias='parentId', nullable=False, description='父级ID')
    title: str = Field(None, nullable=False, description='菜单名称')
    name: str = Field(None, nullable=False, description='前端名称')
    icon: str = Field(None, nullable=False, description='前端图标')
    level: int = Field(None, nullable=False, description='菜单级数')
    hidden: int = Field(None, nullable=False, description='前端隐藏')
    sort: int = Field(None, nullable=False, description='菜单排序')
