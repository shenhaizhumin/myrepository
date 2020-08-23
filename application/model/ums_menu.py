from application.model import Base
import random
from sqlalchemy import Integer, String, SMALLINT, Column, DateTime, Boolean, ForeignKey
from datetime import datetime


class UmsMenu(Base):
    __tablename__ = "ums_menu"
    id = Column("id", Integer, primary_key=True, nullable=False)
    parent_id = Column("parent_id", Integer, nullable=False)
    title = Column("title", String, nullable=False)
    name = Column("name", String, nullable=False)
    icon = Column("icon", String, nullable=False)
    # create_time = Column("create_time", DateTime, default='CURRENT_TIMESTAMP', nullable=False)
    create_time = Column("create_time", DateTime, default=datetime.now(), nullable=False)
    level = Column("level", SMALLINT, nullable=False)
    hidden = Column("hidden", SMALLINT, nullable=False)
    sort = Column("sort", SMALLINT, nullable=False)


class UmsRoleMenuRelation(Base):
    __tablename__ = "ums_role_menu_relation"
    id = Column("id", Integer, primary_key=True, nullable=False)
    role_id = Column("role_id", Integer, nullable=False)
    menu_id = Column("menu_id", Integer, nullable=False)