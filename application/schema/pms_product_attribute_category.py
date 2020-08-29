from pydantic import BaseModel
from typing import List
from application.model.pms_product_attribute_category import PmsProductAttribute


# class PmsProductAttributeSchema(BaseModel):


class PmsProductAttributeCategorySchema(BaseModel):
    '''
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", String, nullable=False, comment='分类名称')
    attribute_count = Column("attribute_count", Integer, default=0, nullable=False, comment='属性数量')
    param_coun
    '''
    id: int
    name: str = None
    attribute_count: int = None
    param_count: int = None
    productAttributeList: List[PmsProductAttribute] = []
