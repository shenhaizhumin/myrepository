from fastapi import APIRouter, Depends, Query, Form, Request
from application.service.oss_service import OssService as oss_service
from application.settings import logger
from application.schema.oss_schema import OssFileSchema, OssFileCallbackSchema
from application.api.response import BaseResponse

oss_router = APIRouter()


@oss_router.get('/policy', description='oss上传签名生成', summary='oss上传签名生成')
async def get_policy(schema: OssFileSchema = Depends()):
    logger.info("/policy")
    logger.info("schema:{}".format(schema.__dict__))
    return BaseResponse.success(oss_service.get_policy(schema))


@oss_router.post('/callback', description='oss上传成功回调', summary='oss上传成功回调')
async def callback(req: Request, schema: OssFileCallbackSchema = Depends()):
    logger.info("/callback")
    logger.info("form:{}".format(await req.form()))
    logger.info("schema:{}".format(schema.__dict__))
    return BaseResponse.success(schema)


@oss_router.post('/decodeCallback', description='解码callback', summary='解码callback')
async def decode_callback(req: Request, callback_str: str = Form(...)):
    logger.info("form:{}".format(await req.form()))
    return BaseResponse.success(oss_service.decode_callback(callback_str))
