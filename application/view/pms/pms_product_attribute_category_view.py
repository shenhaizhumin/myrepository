from fastapi import APIRouter, Depends, Query, Path, Request, Header, Body
from application.model import Session, get_db
from application.api.response import BaseError, BaseResponse
from application.authentication.UsernamePasswordAuthenticationToken import get_current_user, verify_token
from application.service.pms.pms_product_attribute_category_service import \
    PmsProductAttributeCategoryService as category_service
from typing import List

'''
商品属性分类Controller
'''
pms_product_attribute_category = APIRouter()


@pms_product_attribute_category.post('/create', description='添加商品属性分类', summary='添加商品属性分类')
async def create(name: str = Query(...), db=Depends(get_db),
                 user_data=verify_token):
    return BaseResponse.success(category_service.create(db, name))


@pms_product_attribute_category.post('/update/{id}', description='修改商品属性分类', summary='修改商品属性分类')
async def update(category_id: int = Path(..., alias='id'), name: str = Query(...), db=Depends(get_db),
                 user_data=verify_token):
    return BaseResponse.success(category_service.update(db, category_id, name))


@pms_product_attribute_category.get('/delete/{id}', description='删除单个商品属性分类', summary='删除单个商品属性分类')
async def delete(category_id: int = Path(..., alias='id'), db=Depends(get_db),
                 user_data=verify_token):
    return BaseResponse.success(category_service.delete(db, category_id))


@pms_product_attribute_category.get('/{id}', description='获取单个商品属性分类信息', summary='获取单个商品属性分类信息')
async def get_item(category_id: int = Path(..., alias='id'), db=Depends(get_db),
                   user_data=verify_token):
    return BaseResponse.success(category_service.get_item(db, category_id))


@pms_product_attribute_category.get('/list', description='分页获取所有商品属性分类', summary='分页获取所有商品属性分类')
async def get_list(db=Depends(get_db), user_data=verify_token, page_num: int = Query(1, alias='pageNum'),
                   page_size: int = Query(5, alias='pageSize'), ):
    return BaseResponse.success(category_service.get_list(db, page_num, page_size))


@pms_product_attribute_category.get('/list/withAttr', description='获取所有商品属性分类及其下属性', summary='获取所有商品属性分类及其下属性')
async def list_with_attr(db=Depends(get_db), user_data=verify_token):
    return BaseResponse.success(category_service.get_list_with_attr(db))
