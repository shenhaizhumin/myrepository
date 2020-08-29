from application.model import Session, Base
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey
from datetime import datetime

'''
 private Long id;

    @ApiModelProperty(value = "创建时间")
    private Date createTime;

    @ApiModelProperty(value = "资源名称")
    private String name;

    @ApiModelProperty(value = "资源URL")
    private String url;

    @ApiModelProperty(value = "描述")
    private String description;

    @ApiModelProperty(value = "资源分类ID")
    private Long categoryId;
'''


class UmsResource(Base):
    __tablename__ = "ums_resource"
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", String, nullable=False)
    url = Column("url", String, nullable=True)
    description = Column("description", String, nullable=True)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False)
    category_id = Column("category_id", Integer, nullable=False)


# ums_role_resource_relation
class UmsRoleResourceRelation(Base):
    __tablename__ = "ums_role_resource_relation"
    id = Column("id", Integer, primary_key=True, nullable=False)
    role_id = Column("role_id", Integer, nullable=False)
    resource_id = Column("resource_id", Integer, nullable=False)


class UmsResourceCategory(Base):
    '''
    private Long id;

    @ApiModelProperty(value = "创建时间")
    private Date createTime;

    @ApiModelProperty(value = "分类名称")
    private String name;

    @ApiModelProperty(value = "排序")
    private Integer sort;
    '''
    __tablename__ = "ums_resource_category"
    id = Column("id", Integer, primary_key=True, nullable=False)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False, comment='创建时间')
    name = Column("name", String, nullable=False, comment='分类名称')
    sort = Column("sort", Integer, nullable=False, comment='排序')
