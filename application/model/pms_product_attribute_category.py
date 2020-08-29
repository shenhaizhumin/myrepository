from application.model import Base
import random
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

'''
private Long id;

    private String name;

    @ApiModelProperty(value = "属性数量")
    private Integer attributeCount;

    @ApiModelProperty(value = "参数数量")
    private Integer paramCount;
'''


class PmsProductAttributeCategory(Base):
    __tablename__ = "pms_product_attribute_category"
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", String, nullable=False, comment='分类名称')
    attribute_count = Column("attribute_count", Integer, default=0, nullable=False, comment='属性数量')
    param_count = Column("param_count", Integer, nullable=False, default=0, comment='参数数量')
    # product_attribute_list = relationship('PmsProductAttribute', lazy='joined')


'''
private Long id;

    private Long productAttributeCategoryId;

    private String name;

    @ApiModelProperty(value = "属性选择类型：0->唯一；1->单选；2->多选")
    private Integer selectType;

    @ApiModelProperty(value = "属性录入方式：0->手工录入；1->从列表中选取")
    private Integer inputType;

    @ApiModelProperty(value = "可选值列表，以逗号隔开")
    private String inputList;

    @ApiModelProperty(value = "排序字段：最高的可以单独上传图片")
    private Integer sort;

    @ApiModelProperty(value = "分类筛选样式：1->普通；1->颜色")
    private Integer filterType;

    @ApiModelProperty(value = "检索类型；0->不需要进行检索；1->关键字检索；2->范围检索")
    private Integer searchType;

    @ApiModelProperty(value = "相同属性产品是否关联；0->不关联；1->关联")
    private Integer relatedStatus;

    @ApiModelProperty(value = "是否支持手动新增；0->不支持；1->支持")
    private Integer handAddStatus;

    @ApiModelProperty(value = "属性的类型；0->规格；1->参数")
    private Integer type;
'''


class PmsProductAttribute(Base):
    __tablename__ = "pms_product_attribute"

    id = Column("id", Integer, primary_key=True, nullable=False)
    product_attribute_category_id = Column("product_attribute_category_id",
                                           ForeignKey('pms_product_attribute_category.id'),
                                           primary_key=True, nullable=False)
    name = Column("name", String, nullable=False, comment='分类名称')
    select_type = Column("select_type", SMALLINT, nullable=False, comment='属性选择类型：0->唯一；1->单选；2->多选')
    input_type = Column("input_type", SMALLINT, nullable=False, comment='属性录入方式：0->手工录入；1->从列表中选取')
    input_list = Column("input_list", String, nullable=False, comment='可选值列表，以逗号隔开')
    sort = Column('sort', SMALLINT, nullable=False, comment='排序字段：最高的可以单独上传图片')
    filter_type = Column('filter_type', SMALLINT, nullable=False, comment='分类筛选样式：1->普通；2->颜色')
    search_type = Column('search_type', SMALLINT, nullable=False, comment='检索类型；0->不需要进行检索；1->关键字检索；2->范围检索')
    related_status = Column('related_status', SMALLINT, nullable=False, comment='相同属性产品是否关联；0->不关联；1->关联')
    hand_add_status = Column('hand_add_status', SMALLINT, nullable=False, comment='是否支持手动新增；0->不支持；1->支持')
    type = Column('type', SMALLINT, nullable=False, comment='属性的类型；0->规格；1->参数')
