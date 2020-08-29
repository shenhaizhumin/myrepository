from fastapi import HTTPException


class CommonResult(object):
    message: str = 'ok'
    code: int = 200

    def __init__(self, msg='ok', code=200, data=None):
        self.code = code
        self.message = msg
        self.data = data

    @classmethod
    def success(cls, data):
        return CommonResult(data=data)

    # @classmethod
    # def success_flag(cls):
    #     return
