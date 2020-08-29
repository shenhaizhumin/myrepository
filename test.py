from datetime import datetime
import time

# now = datetime.now()
#
# print(now.strftime("%Y--%m--%d %H:%M:%S"))
# print(time.time())
# timestamp = time.mktime(datetime.now().timetuple()) * 1000.0
#
# d = datetime.fromtimestamp(timestamp / 1000)
# arg = {'create': d}
# print(arg)
# arg.update({'create': time.mktime(arg['create'].timetuple()) * 1000.0})
# print(arg)
# print(d)
import logging

# logging.basicConfig(level=logging.DEBUG)
# logging.info("asdasdasd")

from sqlalchemy import create_engine, MetaData, Integer, Column, String, DateTime, SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# from application.settings import mall_db

mall_db = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'mall',
}

# db_url = conf.get('db.url', 'pg_url')
uri = f"mysql+pymysql://{mall_db['user']}:{mall_db['password']}@{mall_db['host']}:{mall_db['port']}/{mall_db['database']}"
engine = create_engine(uri)
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine)
# 建表
# Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


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


from pydantic import BaseModel


class Schema(BaseModel):
    nick_name: str = None
    note: str = None

'''
 测试账号        | NULL                     | 2018-09-29 13:55:30 | 2018-09-29 13:55:39 |      1 |
|  3 | admin        | $2a$10$.E1FokumK5GIXWgKlg.Hc.i/0/2.qdAwYFL1zc5QHdyzpXOr38RZO | http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/images/20180607/timg.jpg | admin@163.com    | 系统管理员      | 系统管理员               | 2018-10-08 13:32:47 | 2020-08-29 11:23:17 |      1 |
|  4 | macro        | $2a$10$Bx4jZPR7GhEpIQfefDQtVeS58GfT5n6mxs/b4nLLK65eMFa16topa | string                                                                      | macro@qq.com     | macro           | macro专用                | 2019-10-06 15:53:51 | 2020-02-03 14:55:55 |      1 |
|  6 | productAdmin | $2a$10$6/.J.p.6Bhn7ic4GfoB5D.pGd7xSiD1a9M6ht6yO0fxzlKJPjRAGm | NULL                                                                        | product@qq.com   | 商品管理员      | 只有商品权限             | 2020-02-07 16:15:08 | NULL                |      1 |
|  7 | orderAdmin   | $2a$10$UqEhA9UZXjHHA3B.L9wNG.6aerrBjC6WHTtbv1FdvYPUI.7lkL6E. | NULL                                                                        | order@qq.com     | 订单管理员      | 只有订单管理权限
'''
# schema = Schema(nick_name='系统管理员', note='系统管理员')
# schema = Schema(nick_name='macro', note='macro专用')
# schema = Schema(nick_name='商品管理员', note='只有商品权限')
schema = Schema(nick_name='测试账号', note='1231231231')
update_args = {k: v for k, v in schema.dict().items() if v}
# print(len(update_args))
# for key in schema.__dict__:
#     value = getattr(schema, key)
#     if value:
#         update_args.update({key: value})
# rows = session.query(UmsAdmin).filter_by(id=3).update(update_args)
# rows = session.query(UmsAdmin).filter_by(id=4).update(update_args)
# rows = session.query(UmsAdmin).filter_by(id=6).update(update_args)
rows = session.query(UmsAdmin).filter_by(id=1).update(update_args)
# print(update_args)
session.commit()
print(rows)
# '''
# SELECT
#             p.*
#         FROM
#             ums_admin_role_relation ar
#             LEFT JOIN ums_role r ON ar.role_id = r.id
#             LEFT JOIN ums_role_permission_relation rp ON r.id = rp.role_id
#             LEFT JOIN ums_permission p ON rp.permission_id = p.id
#         WHERE
#             ar.admin_id = #{adminId}
#             AND p.id IS NOT NULL
#             AND p.id NOT IN (
#                 SELECT
#                     p.id
#                 FROM
#                     ums_admin_permission_relation pr
#                     LEFT JOIN ums_permission p ON pr.permission_id = p.id
#                 WHERE
#                     pr.type = - 1
#                     AND pr.admin_id = #{adminId}
#             )
#         UNION
#         SELECT
#             p.*
#         FROM
#             ums_admin_permission_relation pr
#             LEFT JOIN ums_permission p ON pr.permission_id = p.id
#         WHERE
#             pr.type = 1
#             AND pr.admin_id = #{adminId}
# '''
# result = session.execute('''
# SELECT
#         p.*
#     from
#         ums_admin_role_relation ar
#         left join ums_role r on ar.role_id=r.id
#         left join ums_role_permission_relation rp on r.id=rp.role_id
#         left join ums_permission p on rp.permission_id=p.id
#     where
#         ar.admin_id = :admin_id
#         and p.id is not null
#         and p.id not in(
#             select
#                 p.id
#             from
#                 ums_admin_permission_relation pr
#                 left join ums_permission p on pr.permission_id=p.id
#             where
#                 pr.type=-1
#                 and pr.admin_id=:admin_id
#         )
#     union
#     select
#         p.*
#         from ums_admin_permission_relation apr
#         join ums_permission p on apr.permission_id=p.id
#         where apr.admin_id=:admin_id
# ''', {'admin_id': 3}).fetchall()
# result = session.execute(
#     '''
#     SELECT
#             p.*
#         FROM
#             ums_admin_permission_relation pr
#             LEFT JOIN ums_permission p ON pr.permission_id = p.id
#         WHERE
#             pr.type = 1
#             AND pr.admin_id = :admin_id
#     ''', {'admin_id': 3}).fetchall()
# result = session.execute('select distinct nick_name from ums_admin;').fetchall()
# print(result)
# session.commit()

# args=dict()
# if args.keys()
from pymodm.manager import Manager
from pymodm import MongoModel, fields
from pymodm.connection import connect

uri = 'mongodb://47.106.69.126:27017/test1'


class ResourcesManager(Manager):
    def get_queryset(self):
        # return super().get_queryset().raw({"isDelete": False})
        return super().get_queryset().raw({})


RTYPES = ('folder', 'model', 'texture', 'material', 'cubemap')


class Resources(MongoModel):
    uuid = fields.CharField(required=True, primary_key=True)
    id = fields.CharField(required=True)
    name = fields.CharField()
    type = fields.CharField(required=True, max_length=20, choices=RTYPES)
    userID = fields.IntegerField(min_value=1, required=True)
    spaceID = fields.IntegerField(min_value=1, required=True)
    parentID = fields.CharField()
    projectID = fields.CharField(max_length=80)
    # projectID = ReferenceField(Projects)
    isDelete = fields.BooleanField(default=False)
    version = fields.CharField()
    thumbnail = fields.CharField()
    preload = fields.BooleanField(default=True)
    createTime = fields.FloatField()
    updateTime = fields.FloatField()
    tags = fields.ListField(default=None)
    extensions = fields.DictField(default=None)
    data = fields.DictField(default=None)
    file = fields.DictField(default=None)
    meta = fields.DictField(default=None)
    # project = fields.ReferenceField(Projects, on_delete=fields.ReferenceField.CASCADE)
    objects = ResourcesManager()

    class Meta:
        final = True
        # connection_alias = 'ODM'
        connection_name = 'resources'


from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict, Union
from enum import Enum


class FileTypV(BaseModel):
    filename: Optional[str]
    hash: Optional[str]
    size: Optional[str]
    url: Optional[str]
    variants: Optional[Dict] = None


class ResourceType(Enum):
    folder = "folder"
    model = "model"
    texture = "texture"
    material = "material"
    cubemap = "cubemap"


class ResourceNode(BaseModel):
    name: str = None
    id: str
    type: ResourceType = None
    projectID: str = None
    version: Optional[str] = "0.10.0"
    thumbnail: str = None
    parentID: str = None
    preload: bool = True
    tags: Optional[List] = list()
    extensions: Optional[Dict] = dict()
    data: Optional[Dict] = dict()
    file: Optional[Union[FileTypV, Dict]] = dict()
    meta: Optional[Dict] = dict()
    children: list = []

    # createTime: float = None
    # updateTime: float = None

    class Config:
        orm_mode = True
        use_enum_values = True  # 直接得到枚举类属性的值


connect(uri)


# res = Resources.objects.raw(query).all()


# for r in res:
#     print(r.parentID)

# for root in root_res:
#     print({'parentID': root.parentID, 'name': root.name})


# 根据根结点查出所有子节点
def convert_resource_to_node(resource: Resources, resource_list: list) -> ResourceNode:
    resource_node = ResourceNode.from_orm(resource)
    # resource_node = resource
    children = []
    for res in resource_list:
        if res.parentID == resource.id:
            children.append(convert_resource_to_node(res, resource_list))
    resource_node.children = children
    return resource_node


def append_resource_id(src_ids, src_resource_list):
    print('append_resource_id')
    if len(src_resource_list) == 0:
        return
    for src_res in src_resource_list:
        print(src_res.to_son())
        sub_query = {
            'parentID': src_res.id,
            'projectID': src_res.projectID,
            'spaceID': src_res.spaceID
        }
        src_ids.append(src_res.id)
        child_list = Resources.objects.raw(sub_query).all()
        append_resource_id(src_ids, list(child_list))


def get_list():
    query = {
        'id': '6a6f6af2063b9883bc98599dcbc02a93e1f002b0',
        'spaceID': 968,
        'projectID': '617fb70ad20640661ae026bd6ad96d7a11eaac72',
        # 'type': {'$in': ['model']}
        'isDelete': {'$in': [True, False]}
    }
    # 查出所有节点
    all_resource_list = list(Resources.objects.raw(query).all())
    # print(all_resource_list)
    # for res in all_res_list:
    #     print(res.name)

    # 查出所有根节点
    # root_res = Resources.objects.raw({'projectID': {'$in': [None, '']}}).all()

    # resource_node_list = [convert_resource_to_node(resource, all_resource_list) for resource in all_resource_list if
    #                       not resource.parentID or resource.parentID == '']
    src_ids = []
    append_resource_id(src_ids, all_resource_list)
    print({'count': len(src_ids),
           'src_ids': src_ids})
    return {'count': len(src_ids),
            'src_ids': src_ids}


from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get('/hello')
async def get():
    return get_list()


class DataMapping(BaseModel):
    name: str = None
    material: str = Field(None, alias='resource')

    class Config:
        orm_mode = True


if __name__ == '__main__':
    # import uvicorn
    #
    # uvicorn.run(app, port=8021)
    # get_list()
    # mapping = [{"name": "Cube", "resource": None}]
    # new_mapping = [DataMapping(**m) for m in mapping]
    # for x in new_mapping:
    #     print(x.name)
    # ids = '1'
    # ids = [i for i in ids if i is not None and i != '']
    # print(len(ids))
    args = {
        1: '2'
    }
    print(args[1])
