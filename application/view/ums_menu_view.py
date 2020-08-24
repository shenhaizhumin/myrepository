from fastapi import APIRouter, Query, Path, Depends
from application.schema.ums_menu_schema import UmsMenuSchema, UmsMenuUpdateSchema
from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.service.ums_menu_service import UmsMenuService
from application.model import get_db
from application.api.response import BaseError, BaseResponse

'''
后台菜单管理Service实现类
'''

ums_menu_router = APIRouter()
menu_service = UmsMenuService()


@ums_menu_router.post('/create', summary='添加后台菜单')
async def create_menu(schema: UmsMenuSchema, user_data=Depends(verify_token), db=Depends(get_db)):
    count = await menu_service.create_menu(db, schema)
    return BaseResponse(data=count)


@ums_menu_router.put('/update/{id}', summary='修改后台菜单')
async def update_menu(schema_update: UmsMenuUpdateSchema, menu_id: int = Path(..., alias='id'),
                      user_data=Depends(verify_token), db=Depends(get_db)):
    count = await menu_service.update_menu(db, menu_id, schema_update)
    return BaseResponse(data=count)
