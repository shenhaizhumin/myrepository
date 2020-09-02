from fastapi import APIRouter, Query, Path, Depends, Body
from application.schema.ums_role_schema import UmsRoleSchema, UmsRoleUpdateSchema
# from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.model import get_db
from application.service.ums_role_service import UmsRoleService as role_service
from application.api.response import BaseResponse, BaseError
from typing import List

ums_role_router = APIRouter()


@ums_role_router.post('/create', summary='添加角色')
async def create_cole(schema: UmsRoleSchema, db=Depends(get_db)):
    result = await role_service.create(db, schema)
    return BaseResponse.success(result)


@ums_role_router.post('/update/{id}', summary='修改角色')
async def update_cole(schema: UmsRoleUpdateSchema, role_id=Path(..., alias='id'), db=Depends(get_db)):
    await role_service.update(db, role_id, schema)
    return BaseResponse()


@ums_role_router.post('/delete', summary='批量删除角色')
async def delete_cole(role_ids: List[int] = Body(..., alias='ids'), db=Depends(get_db)):
    result = await role_service.delete(db, role_ids)
    return BaseResponse.success(result)


@ums_role_router.get('/permission/{roleId}', summary='获取相应角色权限')
async def get_permission_list(role_id: int = Path(..., alias='roleId'), db=Depends(get_db)):
    result = await role_service.get_permission_list(db, role_id)
    return BaseResponse.success(result)


@ums_role_router.post('/permission/update', summary='修改角色权限')
async def update_permission(role_id: int = Query(..., alias='roleId'),
                            permission_ids: List[int] = Body(..., alias='ids'),
                            db=Depends(get_db)):
    count = await role_service.update_permission(db, role_id, permission_ids)
    return BaseResponse.success(count)


@ums_role_router.get('/listAll', summary='获取所有角色')
async def list_all(db=Depends(get_db)):
    result = await role_service.list(db)
    return BaseResponse.success(result)


@ums_role_router.get('/list', summary='根据角色名称分页获取角色列表')
async def list_by_keyword(keyword: str = Query(None), page_num: int = Query(1, alias='pageNum'),
                          page_size: int = Query(5, alias='pageSize'), db=Depends(get_db)):
    result = await role_service.list_by_keyword(db, keyword, page_size, page_num)
    return BaseResponse.success(result)


@ums_role_router.post('/updateStatus/{id}', summary='修改角色状态')
async def update_status(role_id=Path(..., alias='id'), status: int = Query(...), db=Depends(get_db)):
    await role_service.update(db, role_id, UmsRoleUpdateSchema(status=status))
    return BaseResponse()


@ums_role_router.get('/listMenu/{roleId}', summary='获取角色相关菜单')
async def list_menu(role_id=Path(..., alias='roleId'), db=Depends(get_db)):
    result = await role_service.list_menu(db, role_id)
    return BaseResponse.success(result)


@ums_role_router.get('/listResource/{roleId}', summary='获取角色相关资源')
async def list_resource(role_id=Path(..., alias='roleId'), db=Depends(get_db)):
    result = await role_service.list_resource(db, role_id)
    return BaseResponse.success(result)


@ums_role_router.post('/allocMenu', summary='给角色分配菜单')
async def alloc_menu(role_id=Query(..., alias='roleId'), menu_ids: List[int] = Body(..., alias='menuIds'),
                     db=Depends(get_db)):
    count = await role_service.alloc_menu(db, role_id, menu_ids)
    return BaseResponse.success(count)


@ums_role_router.post('/allocResource', summary='给角色分配资源')
async def alloc_resource(role_id=Query(..., alias='roleId'), resource_ids: List[int] = Body(..., alias='resourceIds'),
                         db=Depends(get_db)):
    count = await role_service.alloc_resource(db, role_id, resource_ids)
    return BaseResponse.success(count)
