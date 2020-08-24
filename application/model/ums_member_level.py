'''
private Long id;

    private String name;

    private Integer growthPoint;

    @ApiModelProperty(value = "是否为默认等级：0->不是；1->是")
    private Integer defaultStatus;

    @ApiModelProperty(value = "免运费标准")
    private BigDecimal freeFreightPoint;

    @ApiModelProperty(value = "每次评价获取的成长值")
    private Integer commentGrowthPoint;

    @ApiModelProperty(value = "是否有免邮特权")
    private Integer priviledgeFreeFreight;

    @ApiModelProperty(value = "是否有签到特权")
    private Integer priviledgeSignIn;

    @ApiModelProperty(value = "是否有评论获奖励特权")
    private Integer priviledgeComment;

    @ApiModelProperty(value = "是否有专享活动特权")
    private Integer priviledgePromotion;

    @ApiModelProperty(value = "是否有会员价格特权")
    private Integer priviledgeMemberPrice;

    @ApiModelProperty(value = "是否有生日特权")
    private Integer priviledgeBirthday;

    private String note;
'''
from application.model import Base
import random
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey, BIGINT
from datetime import datetime


class UmsMemberLevel(Base):
    __tablename__ = 'ums_member_level'
    id = Column("id", Integer, primary_key=True, nullable=False)
    growth_point = Column("growth_point", Integer, nullable=False)
    default_status = Column("default_status", Integer, nullable=False, comment='是否为默认等级：0->不是；1->是')
    free_freight_point = Column("free_freight_point", BIGINT, nullable=False, comment='免运费标准')
    comment_growth_point = Column("comment_growth_point", Integer, nullable=False, comment='每次评价获取的成长值')
    priviledge_free_freight = Column("priviledge_free_freight", Integer, nullable=False, comment='是否有免邮特权')
    priviledge_sign_in = Column("priviledge_sign_in", Integer, nullable=False, comment='是否有签到特权')
    priviledge_comment = Column("priviledge_comment", Integer, nullable=False, comment='是否有评论获奖励特权')
    priviledge_promotion = Column("priviledge_promotion", Integer, nullable=False, comment='是否有专享活动特权')
    priviledge_member_price = Column("priviledge_member_price", Integer, nullable=False, comment='是否有会员价格特权')
    priviledge_birthday = Column("priviledge_birthday", Integer, nullable=False, comment='是否有生日特权')
    note = Column("note", String, nullable=True)
    name = Column("name", String, nullable=False)
