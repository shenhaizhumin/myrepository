from pydantic import BaseModel, Field


class PmsProductAttributeSchema(BaseModel):
    product_attribute_category_id: int = Field(..., description='商品属性分类id')
    name: str = Field(..., description='属性名称')
    select_type: int = Field(..., description='属性选择类型：0->唯一；1->单选；2->多选')
    input_type: int = Field(..., description='属性录入方式：0->手工录入；1->从列表中选取')
    input_list: str = Field(..., description='可选值列表，以逗号隔开')
    sort: int = Field(..., description='排序字段：最高的可以单独上传图片')
    filter_type: int = Field(..., description='分类筛选样式：1->普通；2->颜色')
    search_type: int = Field(..., description='检索类型；0->不需要进行检索；1->关键字检索；2->范围检索')
    related_status: int = Field(..., description='相同属性产品是否关联；0->不关联；1->关联')
    hand_add_status: int = Field(..., description='是否支持手动新增；0->不支持；1->支持')
    type: int = Field(..., description='属性的类型；0->规格；1->参数')


class PmsProductAttributeUpdateSchema(BaseModel):
    product_attribute_category_id: int = Field(None, description='商品属性分类id')
    name: str = Field(None, description='属性名称')
    select_type: int = Field(None, description='属性选择类型：0->唯一；1->单选；2->多选')
    input_type: int = Field(None, description='属性录入方式：0->手工录入；1->从列表中选取')
    input_list: str = Field(None, description='可选值列表，以逗号隔开')
    sort: int = Field(None, description='排序字段：最高的可以单独上传图片')
    filter_type: int = Field(None, description='分类筛选样式：1->普通；2->颜色')
    search_type: int = Field(None, description='检索类型；0->不需要进行检索；1->关键字检索；2->范围检索')
    related_status: int = Field(None, description='相同属性产品是否关联；0->不关联；1->关联')
    hand_add_status: int = Field(None, description='是否支持手动新增；0->不支持；1->支持')
    type: int = Field(None, description='属性的类型；0->规格；1->参数')
