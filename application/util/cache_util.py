from application.settings import redis_connect


class Cache:
    @classmethod
    async def get_account_session(cls, username: str, user_id: int):
        key = get_token_key(username, user_id)
        value = redis_connect.get(key)
        if not value:
            return None
        return value.decode()

    @classmethod
    async def set_account_session(cls, username: str, user_id: int, token: str):
        key = get_token_key(username, user_id)
        return redis_connect.set(key, token)

    @classmethod
    async def delete_account_session(cls, username: str, user_id: int):
        redis_connect.delete(get_token_key(username, user_id))


def get_token_key(username: str, user_id: int):
    return '{}_{}'.format(username, user_id)


def create_user_data(username: str, user_id: int):
    return {
        'username': username,
        'user_id': user_id
    }
