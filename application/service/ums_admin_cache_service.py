from application.settings import redis_admin, redis_database, redis_expire_common, redis_resource_list, \
    ACCESS_TOKEN_EXPIRE_SECONDS
from application.service.redis_service import RedisService
from application.util.token_util import get_token_key
from application.model.ums_admin import UmsAdmin

redis_service = RedisService()


class UmsAdminCacheService(object):
    @classmethod
    def get_admin(cls, username):
        key = '{}:{}:{}'.format(redis_database, redis_admin, username)
        admin_str = redis_service.get(key)
        print("admin_cache_str:{}".format(admin_str))
        if admin_str:
            return eval(admin_str)
        else:
            return None

    @classmethod
    def set_admin(cls, ums_admin_dict):
        key = '{}:{}:{}'.format(redis_database, redis_admin, ums_admin_dict['username'])
        redis_service.set(key, str(ums_admin_dict).encode(), redis_expire_common)

    @classmethod
    def set_token_by_user_data(cls, username, user_id, token):
        key = get_token_key(username=username, user_id=user_id)
        redis_service.set(key, token, ACCESS_TOKEN_EXPIRE_SECONDS)

    @classmethod
    def get_access_token_by_user(cls, username, user_id) -> str:
        key = get_token_key(username=username, user_id=user_id)
        token = redis_service.get(key)
        if token:
            return token.decode()
        return token

    @classmethod
    def del_access_token(cls, username, user_id):
        redis_service.delete(get_token_key(username=username, user_id=user_id))

    @classmethod
    def delete_admin(cls, username):
        if username:
            key = '{}:{}:{}'.format(redis_database, redis_admin, username)
            redis_service.delete(key)

    # @classmethod
    # def delete_admin_by_id(cls, user_id):
    #     if user_id:
    #         ums_admin=db
    #         key = '{}:{}:{}'.format(redis_database, redis_admin, username)
    #         redis_service.delete(key)

    @classmethod
    def del_resource_list_by_role(cls, role_id):
        pass

    @classmethod
    def del_resource_list_by_role_ids(cls, role_ids):
        pass
