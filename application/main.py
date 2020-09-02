from fastapi import FastAPI, Depends, HTTPException
import uvicorn as u
from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from application.view.ums_admin_view import ums_admin_router
from application.api.response import BaseError
from application.view.ums_member_level_view import ums_member_router
from application.view.ums_menu_view import ums_menu_router
from application.view.ums_permission_view import ums_permission_router
from application.view.ums_resource_category_view import ums_resource_category_router
from application.view.ums_resource_view import ums_resource_router
from application.view.ums_role_view import ums_role_router
from application.view.pms.pms_brand_view import pms_brand_router
from application.view.pms.pms_product_attribute_category_view import pms_product_attribute_category
from starlette.responses import StreamingResponse
from fastapi.exceptions import StarletteHTTPException
import logging
import time
from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.settings import error_logger

app = FastAPI(debug=True)
app.include_router(ums_admin_router, prefix='/admin', tags=['后台用户管理'])
app.include_router(ums_member_router, prefix='/memberLevel', tags=['会员等级管理Controller'],
                   dependencies=[Depends(verify_token)])
app.include_router(ums_menu_router, prefix='/menu', tags=['后台菜单管理Controller'], dependencies=[Depends(verify_token)])
app.include_router(ums_permission_router, prefix='/permission', tags=['后台用户权限管理'], dependencies=[Depends(verify_token)])
app.include_router(ums_resource_category_router, prefix='/resourceCategory', tags=['后台资源分类管理Controller'],
                   dependencies=[Depends(verify_token)])
app.include_router(ums_resource_router, prefix='/resource', tags=['后台用户角色管理'], dependencies=[Depends(verify_token)])
app.include_router(pms_brand_router, prefix='/brand', tags=['商品品牌管理'], dependencies=[Depends(verify_token)])
app.include_router(pms_product_attribute_category, prefix='/productAttribute/category', tags=['商品属性分类管理'],
                   dependencies=[Depends(verify_token)])

# 后台用户角色管理
app.include_router(ums_role_router, prefix='/role')

# app.mount("/static", StaticFiles(directory="static"), name="static")
#
# # 创建一个templates（模板）对象，以后可以重用。
# templates = Jinja2Templates(directory="templates")

'''
postgres=# drop database mall ;
DROP DATABASE
postgres=# create database mall owner zengqi;
CREATE DATABASE
postgres=# grant ALL privileges on database mall to zengqi;
GRANT
'''

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


# 中间件
@app.middleware("http")
async def log_request_params(request: Request, call_next) -> StreamingResponse:
    """记录输入参数，统计耗时"""
    logger.info(">>>>>>>>>>>>>>>>>>>>>>>")
    logger.info(f"++++++{request.url}++++++++")
    logger.info(f"===>headers:{request.headers}")
    logger.info(f"===>path_params:{request.path_params}")
    logger.info(f"===>query_params:{request.query_params}")
    # logger.info(f"===>body:{await request.body()}")
    # logger.info(f"===>form:{await request.form()}")
    start_time = time.time()
    response = await call_next(request)
    logger.info(f"总耗时： {time.time() - start_time}")
    # logger.info(f"+++>{response.render()}")
    logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<")
    return response


# Request在路径操作中声明一个参数，该参数将返回模板。
# 使用templates您创建的渲染并返回TemplateResponse，并request在Jinja2“上下文” 中将用作键值对之一。
# @app.get("/items/{id}")
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.exception_handler(BaseError)
async def unicorn_exception_handler(request: Request, exc: BaseError):
    # logger.error(exc.message)
    error_logger.error(exc.message)
    return JSONResponse(
        status_code=200,
        content={"message": exc.message, "code": exc.code},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException):
    error_logger.error(exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail, "code": -200})


@app.exception_handler(RequestValidationError)
async def handle_exception(request: Request, exc: RequestValidationError):
    error_logger.error(exc.errors())
    return JSONResponse(status_code=400, content={"message": "参数有误：{}".format(exc.errors()), "code": -200})


if __name__ == '__main__':
    u.run(app, host="127.0.0.1", port=8030)
