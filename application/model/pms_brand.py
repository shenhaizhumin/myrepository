from application.model import Base
import random
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey
from datetime import datetime

'''
private Long id;

    private String name;

    @ApiModelProperty(value = "首字母")
    private String firstLetter;

    private Integer sort;

    @ApiModelProperty(value = "是否为品牌制造商：0->不是；1->是")
    private Integer factoryStatus;

    private Integer showStatus;

    @ApiModelProperty(value = "产品数量")
    private Integer productCount;

    @ApiModelProperty(value = "产品评论数量")
    private Integer productCommentCount;

    @ApiModelProperty(value = "品牌logo")
    private String logo;

    @ApiModelProperty(value = "专区大图")
    private String bigPic;

    @ApiModelProperty(value = "品牌故事")
    private String brandStory;
'''


class PmsBrand(Base):
    __tablename__ = "pms_brand"
    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", String, nullable=False, comment='品牌名称')
    first_letter = Column("first_letter", String, nullable=False, comment='首字母')
    logo = Column("logo", String, nullable=False, comment='品牌logo')
    big_pic = Column("big_pic", String, nullable=True, comment='专区大图')
    brand_story = Column("brand_story", String, nullable=False, comment='品牌故事')
    sort = Column("sort", SMALLINT, nullable=False)
    show_status = Column("show_status", SMALLINT, nullable=False)
    product_count = Column("product_count", Integer, nullable=False, default=0, comment='产品数量')
    product_comment_count = Column("product_comment_count", Integer, default=0, nullable=False, comment='产品评论数量')
    factory_status = Column("factory_status", SMALLINT, nullable=False, comment='是否为品牌制造商：0->不是；1->是')
