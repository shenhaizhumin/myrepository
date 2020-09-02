import os
import configparser
import redis
from passlib.context import CryptContext

cur_path = os.path.abspath(os.path.curdir)
print(cur_path)
# 当前文件的父路径
father_path = os.path.abspath(os.path.dirname(cur_path) + os.path.sep + ".")
print(father_path)
# conf_path = os.path.join(os.path.join(cur_path, 'application'), 'etc', 'config.ini')
conf_path = os.path.join(cur_path, 'etc', 'config.ini')
print(conf_path)
# 读取配置信息
conf = configparser.ConfigParser()
conf.read(conf_path)

files_conf = dict()
for k in conf.options("file"):
    files_conf[k] = conf.get("file", k)
image_dirname = files_conf['image_dirname']
domain_name = files_conf['domain_name']

"""
    redis config
"""
redis_conf = dict()
for k in conf.options("redis"):
    redis_conf[k] = conf.get("redis", k)
redis_connect = redis.Redis(**redis_conf)
"""
    jwt config
"""
jwt_conf = dict()
for k in conf.options("jwt.extras"):
    jwt_conf[k] = conf.get("jwt.extras", k)

"""
admin 缓存配置
"""
redis_key_conf = dict()
for k in conf.options("redis.key"):
    redis_key_conf[k] = conf.get("redis.key", k)
redis_database = redis_key_conf.get('database')
redis_admin = redis_key_conf.get('admin')
redis_resource_list = redis_key_conf.get('resource_list')
redis_expire_common = redis_key_conf.get('expire_common')

ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 24 * 60
SECRET_KEY = jwt_conf['secret_key']
ALGORITHM = jwt_conf['algorithm']
tokenUrl = '/login'
token_head = 'Bearer '

error_code = -200

jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}

mall_db = dict()
for k in conf.options('db.mall'):
    mall_db[k] = conf.get('db.mall', k)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import logging
from logging import FileHandler

# logging.basicConfig(filename='../log/app_info.log', level=logging.DEBUG,
#                     format='[%(asctime)s][pid:%(process)d][tid:%(thread)d][%(filename)s:%(lineno)d] %(levelname)s: %(message)s')
format_file = '[%(asctime)s][pid:%(process)d][tid:%(thread)d][%(filename)s:%(lineno)d] %(levelname)s: %(message)s'
logger = logging.getLogger('info_log')
logger.setLevel(logging.DEBUG)
file_handler = FileHandler(filename='../log/app_info.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(format_file))
logger.addHandler(file_handler)

error_logger = logging.getLogger('error_log')
file_handler = FileHandler(filename='../log/app_error.log', mode='w')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(format_file))
error_logger.addHandler(file_handler)
