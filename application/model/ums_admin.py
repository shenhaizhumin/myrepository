'''
private Long id;

    private String username;

    private String password;

    @ApiModelProperty(value = "头像")
    private String icon;

    @ApiModelProperty(value = "邮箱")
    private String email;

    @ApiModelProperty(value = "昵称")
    private String nickName;

    @ApiModelProperty(value = "备注信息")
    private String note;

    @ApiModelProperty(value = "创建时间")
    private Date createTime;

    @ApiModelProperty(value = "最后登录时间")
    private Date loginTime;

    @ApiModelProperty(value = "帐号启用状态：0->禁用；1->启用")
    private Integer status;
'''
from application.model import Base
import random
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey
from datetime import datetime


class UmsAdmin(Base):
    __tablename__ = "ums_admin"
    id = Column("id", Integer, primary_key=True, nullable=False)
    username = Column("username", String, nullable=False)
    password = Column("password", String, nullable=False)
    icon = Column("icon", String, nullable=True)
    email = Column("email", String, nullable=False)
    nick_name = Column("nick_name", String, nullable=True)
    note = Column("note", String, nullable=True)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False)
    login_time = Column("login_time", DateTime, default=datetime.now(), nullable=False)
    status = Column("status", SMALLINT, nullable=False)


class UmsRole(Base):
    __tablename__ = "ums_role"
    id = Column("id", Integer, primary_key=True, nullable=False)  #
    name = Column("name", String, nullable=False)
    description = Column("description", String, nullable=False)
    admin_count = Column("admin_count", Integer, nullable=False)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False)
    status = Column("status", SMALLINT, nullable=False)
    sort = Column("sort", SMALLINT, nullable=False)


class UmsAdminRoleRelation(Base):
    __tablename__ = "ums_admin_role_relation"
    id = Column("id", Integer, primary_key=True, nullable=False)
    role_id = Column("role_id", Integer, nullable=False)  #
    admin_id = Column("admin_id", Integer, nullable=False)


'''
private Long id;

    private Long adminId;

    private Date createTime;

    private String ip;

    private String address;

    @ApiModelProperty(value = "浏览器登录类型")
    private String userAgent;
'''


class UmsAdminLoginLog(Base):
    __tablename__ = "ums_admin_login_log"
    id = Column("id", Integer, primary_key=True, nullable=False)
    admin_id = Column("admin_id", Integer, nullable=False)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False)
    ip = Column("ip", String, nullable=True)
    address = Column("address", String, nullable=True)
    user_agent = Column("user_agent", String, nullable=True)


class UmsRolePermissionRelation(Base):
    __tablename__ = "ums_role_permission_relation"
    id = Column("id", Integer, primary_key=True, nullable=False)
    role_id = Column("role_id", Integer, nullable=False)  #
    permission_id = Column("permission_id", Integer, nullable=False)


class UmsAdminPermissionRelation(Base):
    '''
    用户和权限的关系表
    '''
    __tablename__ = "ums_admin_permission_relation"
    id = Column("id", Integer, primary_key=True, nullable=False)
    permission_id = Column("permission_id", Integer, nullable=False)
    admin_id = Column("admin_id", Integer, nullable=False)
    type = Column("type", Integer, nullable=False)


class UmsPermission(Base):
    __tablename__ = 'ums_permission'
    id = Column("id", Integer, primary_key=True, nullable=False)
    pid = Column("pid", Integer, nullable=False)
    name = Column("name", String, nullable=True)
    value = Column("value", String, nullable=True)
    icon = Column("icon", String, nullable=True)
    uri = Column("uri", String, nullable=True)
    type = Column("type", Integer, nullable=False)
    status = Column("status", Integer, nullable=False)
    sort = Column("sort", Integer, nullable=False)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False)
