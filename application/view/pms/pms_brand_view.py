from fastapi import APIRouter, Depends, Query, Path, Request, Header, Body
from application.schema.pms_brand_schema import PmsBrandUpdateSchema, PmsBrandSchema
from application.model import Session, get_db
from application.api.response import BaseError, BaseResponse
from application.authentication.UsernamePasswordAuthenticationToken import get_current_user, verify_token
from application.service.pms.pms_brand_service import PmsBrandService as brand_service
from typing import List

'''
商品品牌管理
'''
pms_brand_router = APIRouter()


@pms_brand_router.get('/listAll', description='获取全部品牌列表', summary='获取全部品牌列表')
async def all_list(db=Depends(get_db), user_data=verify_token):
    return BaseResponse.success(brand_service.list_all(db))


@pms_brand_router.post('/create', description='添加品牌', summary='添加')
async def create_brand(schema: PmsBrandSchema, db=Depends(get_db), user_data=verify_token):
    return BaseResponse.success(brand_service.create_brand(db, schema))


@pms_brand_router.post('/update/{id}', description='更新品牌', summary='更新')
async def update_brand(schema: PmsBrandUpdateSchema, brand_id: int = Path(..., alias='id'), db=Depends(get_db),
                       user_data=verify_token):
    return BaseResponse.success(brand_service.update_brand(db, brand_id, schema))


@pms_brand_router.get('/delete/{id}', description='删除品牌', summary='删除')
async def delete_brand(brand_id: int = Path(..., alias='id'), db=Depends(get_db),
                       user_data=verify_token):
    rows = brand_service.delete_brand(db, brand_id)
    if rows:
        return BaseResponse.success(rows)
    else:
        return BaseResponse.failed('删除操作失败！')


@pms_brand_router.get('/list', description='根据品牌名称分页获取品牌列表', summary='根据品牌名称分页获取品牌列表')
async def brand_list(keyword: str = Query(None), page_num: int = Query(1, alias='pageNum'),
                     page_size: int = Query(5, alias='pageSize'),
                     db=Depends(get_db), user_data=verify_token):
    return BaseResponse.success(brand_service.list_brand(db, keyword, page_num, page_size))


@pms_brand_router.get('/{id}', description='根据编号查询品牌信息', summary='根据编号查询品牌信息')
async def get_brand(brand_id: int = Path(..., alias='id'), db=Depends(get_db),
                    user_data=verify_token):
    return BaseResponse.success(brand_service.get_brand(db, brand_id))


@pms_brand_router.post('/delete/batch', description='批量删除品牌', summary='批量删除品牌')
async def delete_brands(ids: List[int] = Query(...), db=Depends(get_db),
                        user_data=verify_token):
    # return BaseResponse.success(brand_service.delete_brands(db, ids))
    rows = brand_service.delete_brands(db, ids)
    if rows:
        return BaseResponse.success(rows)
    else:
        return BaseResponse.failed('删除操作失败！')
