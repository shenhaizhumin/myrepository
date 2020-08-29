from fastapi import APIRouter, Query, Path, Depends, Body
from application.schema.ums_permission_schema import UmsPermissionSchema, UmsPermissionUpdateSchema
from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.model import get_db
from application.service.ums_permission_service import UmsPermissionService
from application.api.response import BaseResponse, BaseError
from typing import List

ums_permission_router = APIRouter()

permission_service = UmsPermissionService()


@ums_permission_router.post('/create', summary='添加权限')
async def create_permission(schema: UmsPermissionSchema, db=Depends(get_db), user_data=Depends(verify_token)):
    count = await permission_service.create_permission(db, schema)
    return BaseResponse.success(count)


@ums_permission_router.post('/update/{id}', summary='修改权限')
async def update_permission(schema: UmsPermissionUpdateSchema, permission_id: int = Path(..., alias='id'),
                            db=Depends(get_db), user_data=Depends(verify_token)):
    result = await permission_service.update_permission(db, permission_id, schema)
    return BaseResponse.success(result)


@ums_permission_router.post('/delete', summary='根据id批量删除权限')
async def delete_permission(permission_ids: List[int] = Body(...), db=Depends(get_db), user_data=Depends(verify_token)):
    count = await permission_service.delete_permission(db, permission_ids)
    return BaseResponse.success(count)


@ums_permission_router.get('/treeList', summary='以层级结构返回所有权限')
async def get_tree_list(db=Depends(get_db), user_data=Depends(verify_token)):
    tree_list = await permission_service.permission_tree_list(db)
    return BaseResponse.success(tree_list)


@ums_permission_router.get('/list', summary='获取所有权限列表')
async def get_permission_list(db=Depends(get_db), user_data=Depends(verify_token)):
    permission_list = await permission_service.permission_list(db)
    return BaseResponse.success(permission_list)
