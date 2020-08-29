from fastapi import APIRouter, Query, Path, Depends, Body
from application.schema.ums_resource_category_schema import UmsResourceCategorySchema, UmsResourceCategoryUpdateSchema
from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.model import get_db
from application.service.ums_resource_category_service import UmsResourceCategoryService
from application.api.response import BaseResponse, BaseError

ums_resource_category_router = APIRouter()
category_service = UmsResourceCategoryService()


@ums_resource_category_router.get('/listAll', summary='查询所有后台资源分类')
async def list_all(db=Depends(get_db), user_data=Depends(verify_token)):
    category_list = await category_service.list_all(db)
    return BaseResponse.success(category_list)


@ums_resource_category_router.post('/create', summary='添加后台资源分类')
async def a(schema: UmsResourceCategorySchema, db=Depends(get_db), user_data=Depends(verify_token)):
    await category_service.create_category(db, schema)
    return BaseResponse.success('操作成功！')


@ums_resource_category_router.post('/update/{id}', summary='修改后台资源分类')
async def update_category(schema: UmsResourceCategoryUpdateSchema, category_id: int = Path(..., alias='id'),
                          db=Depends(get_db),
                          user_data=Depends(verify_token)):
    category = await category_service.update_category(db, category_id, schema)
    return BaseResponse.success(category)


@ums_resource_category_router.post('/delete/{id}', summary='根据ID删除后台资源')
async def delete_category(category_id: int = Path(..., alias='id'), db=Depends(get_db),
                          user_data=Depends(verify_token)):
    count = await category_service.delete_category(db, category_id)
    return BaseResponse.success(count)
