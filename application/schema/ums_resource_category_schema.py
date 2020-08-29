from pydantic import BaseModel, Field


class UmsResourceCategorySchema(BaseModel):
    '''
    id = Column("id", Integer, primary_key=True, nullable=False)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False, comment='创建时间')
    name = Column("name", String, nullable=False, comment='分类名称')
    sort = Column("sort", Integer, nullable=False, comment='排序')
    '''
    name: str = Field(..., description='分类名称')
    sort: int = Field(..., description='排序')


class UmsResourceCategoryUpdateSchema(BaseModel):
    name: str = Field(None, description='分类名称')
    sort: int = Field(None, description='排序')
