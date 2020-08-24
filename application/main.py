from fastapi import FastAPI
import uvicorn as u
from starlette.requests import Request
# from starlette.staticfiles import StaticFiles
# from starlette.templating import Jinja2Templates
from application.view.ums_admin_view import ums_admin_router
from application.api.response import BaseError
from fastapi.responses import JSONResponse
from application.view.ums_member_level_view import ums_member_router

app = FastAPI(debug=True)
app.include_router(ums_admin_router, prefix='/admin')
app.include_router(ums_member_router, prefix='/memberLevel')

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


# Request在路径操作中声明一个参数，该参数将返回模板。
# 使用templates您创建的渲染并返回TemplateResponse，并request在Jinja2“上下文” 中将用作键值对之一。
# @app.get("/items/{id}")
# async def read_item(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

@app.exception_handler(BaseError)
async def unicorn_exception_handler(request: Request, exc: BaseError):
    # logger.error(exc.message)
    return JSONResponse(
        status_code=200,
        content={"message": exc.message, "code": exc.code},
    )


if __name__ == '__main__':
    u.run(app, host="127.0.0.1", port=8000)
