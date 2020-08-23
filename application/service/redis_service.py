from application.settings import redis_conf
import redis
from datetime import timedelta

redis_connect = redis.Redis(**redis_conf)


class RedisService(object):
    @classmethod
    def get(cls, key: str):
        return redis_connect.get(key)

    @classmethod
    def set(cls, key, obj_value, expire: int = None):
        print("redis-expire:{}".format(expire))
        if expire:
            redis_connect.set(key, obj_value, expire)
        else:
            redis_connect.set(key, obj_value)

    @classmethod
    def delete(cls, key):
        redis_connect.delete(key)

    # @classmethod
    # def get_expire(cls):
    #     redis_connect.get
