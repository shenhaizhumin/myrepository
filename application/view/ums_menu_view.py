from fastapi import APIRouter, Query, Path, Depends
from application.schema.ums_menu_schema import UmsMenuSchema, UmsMenuUpdateSchema
# from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.service.ums_menu_service import UmsMenuService
from application.model import get_db
from application.api.response import BaseError, BaseResponse

'''
后台菜单管理Service实现类
'''

ums_menu_router = APIRouter()
menu_service = UmsMenuService()


@ums_menu_router.post('/create', summary='添加后台菜单')
async def create_menu(schema: UmsMenuSchema, db=Depends(get_db)):
    count = await menu_service.create_menu(db, schema)
    return BaseResponse(data=count)


@ums_menu_router.post('/update/{id}', summary='修改后台菜单')
async def update_menu(schema_update: UmsMenuUpdateSchema, menu_id: int = Path(..., alias='id'),
                      db=Depends(get_db)):
    count = await menu_service.update_menu(db, menu_id, schema_update)
    if count:
        return BaseResponse.success(count)
    else:
        return BaseResponse.failed('菜单修改失败！')


@ums_menu_router.post('/delete/{id}', summary='根据id删除菜单')
async def delete_menu(menu_id: int = Path(..., alias='id'), db=Depends(get_db)):
    count = await menu_service.delete_menu(db, menu_id)
    return BaseResponse.success(count)


@ums_menu_router.get('/{id}', summary='根据ID获取菜单详情')
async def get_menu(*, menu_id: int = Path(..., alias='id'), db=Depends(get_db)):
    ums_menu = await menu_service.get_menu_by_id(db, menu_id)
    if ums_menu:
        return BaseResponse(data=ums_menu)
    else:
        return BaseError(msg='菜单不存在！')


@ums_menu_router.get('/list/{parentId}', summary='分页查询后台菜单')
async def menu_list(*, parent_id: int = Path(..., alias='parentId'),
                    page_num: int = Query(1, alias='pageNum'),
                    page_size: int = Query(5, alias='pageSize'),
                    db=Depends(get_db)):
    menus = await menu_service.menu_list(db, parent_id, page_num, page_size)
    return BaseResponse.success(menus)


@ums_menu_router.get('/tree/list', summary='树形结构返回所有菜单列表')
async def tree_list(*, db=Depends(get_db)):
    menus_tree = await menu_service.tree_list(db)
    return BaseResponse.success(menus_tree)


@ums_menu_router.post('/updateHidden/{id}', summary='修改菜单显示状态')
async def update_hidden(menu_id: int = Path(..., alias='id', description='菜单id'),
                        hidden: int = Query(..., description='前端显示状态'),
                        db=Depends(get_db)):
    count = await menu_service.update_hidden(db, menu_id, hidden)
    return BaseResponse.success(count)
