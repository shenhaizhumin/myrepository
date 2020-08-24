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

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
'''
SELECT
            p.*
        FROM
            ums_admin_role_relation ar
            LEFT JOIN ums_role r ON ar.role_id = r.id
            LEFT JOIN ums_role_permission_relation rp ON r.id = rp.role_id
            LEFT JOIN ums_permission p ON rp.permission_id = p.id
        WHERE
            ar.admin_id = #{adminId}
            AND p.id IS NOT NULL
            AND p.id NOT IN (
                SELECT
                    p.id
                FROM
                    ums_admin_permission_relation pr
                    LEFT JOIN ums_permission p ON pr.permission_id = p.id
                WHERE
                    pr.type = - 1
                    AND pr.admin_id = #{adminId}
            )
        UNION
        SELECT
            p.*
        FROM
            ums_admin_permission_relation pr
            LEFT JOIN ums_permission p ON pr.permission_id = p.id
        WHERE
            pr.type = 1
            AND pr.admin_id = #{adminId}
'''
result = session.execute('''
SELECT
        p.*
    from
        ums_admin_role_relation ar
        left join ums_role r on ar.role_id=r.id
        left join ums_role_permission_relation rp on r.id=rp.role_id
        left join ums_permission p on rp.permission_id=p.id
    where
        ar.admin_id = :admin_id
        and p.id is not null
        and p.id not in(
            select
                p.id
            from
                ums_admin_permission_relation pr
                left join ums_permission p on pr.permission_id=p.id
            where
                pr.type=-1
                and pr.admin_id=:admin_id
        )
    union
    select
        p.*
        from ums_admin_permission_relation apr
        join ums_permission p on apr.permission_id=p.id
        where apr.admin_id=:admin_id
''', {'admin_id': 3}).fetchall()
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
result = session.execute('select distinct nick_name from ums_admin;').fetchall()
print(result)
session.commit()
