from pydantic import BaseModel, ValidationError
from fastapi import HTTPException


class BaseResponse:
    message: str
    code: int

    def __init__(self, msg='ok', code=200, data=None):
        self.message = msg
        self.code = code
        if type(data) == list:
            self.data = data
        if data:
            self.data = data

    @classmethod
    def success(cls, data):
        return BaseResponse(data=data)

    @classmethod
    def failed(cls, msg, data=None):
        # cls.code = -200
        # cls.message = msg
        return BaseResponse(data=data, code=-200, msg=msg)


class BaseError(HTTPException):
    def __init__(self, msg=None, code=-200, status_code=None):
        self.message = msg
        # self.detail = msg
        self.code = code
        self.status_code = status_code


# class BaseValidationError(ValidationError):
'''
private Integer pageNum;
    private Integer pageSize;
    private Integer totalPage;
    private Long total;
    private List<T> list;
'''


class CommonPage(object):
    pageNum: int
    pageSize: int
    totalPage: int
    total: int
    list: list

    def __init__(self, **kwargs):
        self.list = kwargs.get('list')
        self.total = kwargs.get('total')
        self.pageNum = kwargs.get('page_num')
        self.pageSize = kwargs.get('page_size')
        self.totalPage = kwargs.get('total_page')
