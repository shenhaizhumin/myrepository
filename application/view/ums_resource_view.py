from fastapi import APIRouter, Query, Path, Depends, Body
from application.schema.ums_resource_schema import UmsResourceSchema, UmsResourceUpdateSchema
# from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.model import get_db
from application.service.ums_resource_service import UmsResourceService
from application.api.response import BaseResponse, BaseError

ums_resource_router = APIRouter()
resource_service = UmsResourceService()


@ums_resource_router.post('/create', summary='添加后台资源')
async def create_resource(schema: UmsResourceSchema, db=Depends(get_db)):
    await resource_service.create_resource(db, schema)
    return BaseResponse.success()


@ums_resource_router.post('/update/{id}', summary='修改后台资源')
async def update_resource(schema: UmsResourceUpdateSchema, resource_id: int = Path(..., alias='id'), db=Depends(get_db)):
    result = await resource_service.update_resource(db, resource_id, schema)
    return BaseResponse.success(result)


@ums_resource_router.post('/delete/{id}', summary='根据ID删除后台资源')
async def create_resource(resource_id: int = Path(..., alias='id'), db=Depends(get_db)):
    count = await resource_service.delete_resource(db, resource_id)
    return BaseResponse.success(count)


# category_id, name_keyword, url_keyword, page_num, page_size
@ums_resource_router.get('/list', summary='分页模糊查询后台资源')
async def list_query(category_id: int = Query(..., alias='categoryId'),
                     name_keyword: str = Query(None, alias='nameKeyword'),
                     url_keyword: str = Query(None, alias='urlKeyword'),
                     page_num: int = Query(1, alias='pageNum'),
                     page_size: int = Query(5, alias='pageSize'),
                     db=Depends(get_db)):
    result = await resource_service.list_query(db, category_id, name_keyword, url_keyword, page_num, page_size)
    return BaseResponse.success(result)


@ums_resource_router.get('/listAll', summary='查询所有后台资源')
async def list_all(db=Depends(get_db)):
    result = await resource_service.list_all(db)
    return BaseResponse.success(result)


@ums_resource_router.get('/{id}', summary='根据ID获取资源详情')
async def get_resource_by_id(resource_id: int = Path(..., alias='id'), db=Depends(get_db)):
    result = await resource_service.get_resource_by_id(db, resource_id)
    if not result:
        raise BaseError(msg='not found')
    return BaseResponse.success(result)
