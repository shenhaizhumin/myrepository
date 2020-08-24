from fastapi import APIRouter, Depends, Query, Path, Request, Header, Body
from application.settings import token_head, error_code, tokenUrl
from application.schema.ums_admin_schema import UmsAdminInSchema, UmsAdminOutSchema, UmsAdminUpdateSchema, \
    UpdateAdminPasswordSchema, UmsAdminLoginSchema
from application.model import Session, get_db
from application.service.ums_admin_service import UmsAdminService
from application.api.response import BaseError, BaseResponse
from application.authentication.UsernamePasswordAuthenticationToken import get_current_user, verify_token
from application.service.ums_role_service import UmsRoleService
from application.model.ums_admin import UmsAdmin
from typing import List

ums_admin_router = APIRouter()
admin_service = UmsAdminService()
role_service = UmsRoleService()


@ums_admin_router.post('/register', description="用户注册",summary='注册')
async def register(schema: UmsAdminInSchema, db: Session = Depends(get_db)):
    ums_admin = await admin_service.register(db=db, schema=schema)
    if ums_admin:
        return BaseResponse(data=ums_admin)
    else:
        raise BaseError(msg="操作失败！")


@ums_admin_router.post(tokenUrl, description='用户登录',summary='登录')
async def login(schema: UmsAdminLoginSchema, req: Request, db: Session = Depends(get_db)):
    token = await admin_service.login(db=db, username=schema.username, password=schema.password, request=req)
    if not token:
        raise BaseError(code=error_code, msg='用户名或密码错误')
    return BaseResponse(data={
        'token': token,
        'tokenHead': token_head
    })


@ums_admin_router.get('/info', summary='获取当前登录用户信息')
async def get_admin_info(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    menus = await role_service.get_menu_list(db=db, admin_id=current_user.id)
    roles = await admin_service.get_role_list(db=db, admin_id=current_user.id)
    data = (await admin_service.get_admin_by_username(db, current_user.username)).__dict__
    data.update({'menus': menus})
    if roles and len(roles) > 0:
        data.update({'roles': [r.name for r in roles]})
    return BaseResponse(data=data)


@ums_admin_router.post('/logout', summary='登出功能')
async def logout(current_user=Depends(get_current_user)):
    if not await admin_service.logout(current_user.username, current_user.id):
        raise BaseError(msg='操作失败！')
    return BaseResponse()


@ums_admin_router.get('/list', summary='根据用户名或姓名分页获取用户列表')
async def get_list(page_num: int = Query(1, alias='pageNum'), page_size: int = Query(5, alias='pageSize'),
                   keyword: str = Query(None),
                   user_data=Depends(verify_token), db: Session = Depends(get_db)):
    users = await admin_service.list(db=db, page_num=page_num, page_size=page_size,
                                     keyword=keyword)
    print("users:{}".format(users))
    return BaseResponse(data=users)


@ums_admin_router.get('/{id}', summary='获取指定用户信息')
async def get_item(user_id: int = Path(..., alias='id'), user_data=Depends(verify_token),
                   db: Session = Depends(get_db)):
    ums_user = await admin_service.get_admin_by_id(db=db, user_id=user_id)
    return BaseResponse(data=ums_user)


@ums_admin_router.post('/update/{id}', summary='修改指定用户信息')
async def update_user(user_info: UmsAdminUpdateSchema, user_id: int = Path(..., alias='id'),
                      user_data=Depends(verify_token),
                      db: Session = Depends(get_db)):
    await admin_service.update(db=db, user_id=user_id, user_info=user_info)
    return BaseResponse()


@ums_admin_router.post('/updatePassword')
async def update_pwd(pwd_info: UpdateAdminPasswordSchema, current_user=Depends(get_current_user),
                     db: Session = Depends(get_db)):
    if not pwd_info.username:
        pwd_info.username = current_user.username
    if await admin_service.update_password(db=db, pwd_info=pwd_info):
        return BaseResponse()
    else:
        return BaseError(msg='操作失败!')


@ums_admin_router.post('/refreshToken', summary='刷新1token功能')
async def refresh_token(authorization_token: str = Header(..., alias='Authorization')):
    new_token = await admin_service.refresh_token(token=authorization_token)
    if not new_token:
        raise BaseError('token 已过期')
    else:
        return BaseResponse(data={
            'token': new_token,
            'tokenHead': token_head
        })


@ums_admin_router.post('/delete/{id}', summary='删除指定用户信息')
async def delete_ums_admin(user_id: int = Path(..., alias='id'), user_data=Depends(verify_token),
                           db: Session = Depends(get_db)):
    await admin_service.delete(db=db, user_id=user_id)
    return BaseResponse()


@ums_admin_router.post('/updateStatus/{id}', summary='修改帐号状态')
async def update_status(user_id: int = Path(..., alias='id'), status: int = Query(...),
                        user_data=Depends(verify_token),
                        db: Session = Depends(get_db)):
    ums_admin = UmsAdmin(status=status)
    await admin_service.update(db=db, user_id=user_id, user_info=ums_admin)
    return BaseResponse()


@ums_admin_router.post('/role/update', summary='给用户分配角色')
async def update_role(admin_id: int = Query(...), roles: List[int] = Query(...), user_data=Depends(verify_token),
                      db: Session = Depends(get_db)):
    if len(roles) == 0:
        raise BaseError()
    count = await admin_service.update_role(db=db, admin_id=admin_id, roles=roles)
    if count == 0:
        raise BaseError()
    else:
        return BaseResponse()


'''
 @ApiOperation("获取指定用户的角色")
    @RequestMapping(value = "/role/{adminId}", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<List<UmsRole>> getRoleList(@PathVariable Long adminId) {
        List<UmsRole> roleList = adminService.getRoleList(adminId);
        return CommonResult.success(roleList);
    }
'''


@ums_admin_router.get('/role/{adminId}', summary='获取指定用户的角色')
async def get_role_list(admin_id: int = Path(..., alias='adminId'), user_data=Depends(verify_token),
                        db: Session = Depends(get_db)):
    roles = await admin_service.get_role_list(db=db, admin_id=admin_id)
    return BaseResponse(data=[r.name for r in roles])


'''
@ApiOperation("给用户分配+-权限")
    @RequestMapping(value = "/permission/update", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult updatePermission(@RequestParam Long adminId,
                                         @RequestParam("permissionIds") List<Long> permissionIds) {
        int count = adminService.updatePermission(adminId, permissionIds);
        if (count > 0) {
            return CommonResult.success(count);
        }
        return CommonResult.failed();
    }
'''


@ums_admin_router.post('/permission/update', summary='给用户分配+-权限')
async def update_permission(admin_id: int = Query(..., alias='adminId'), permission_ids: List[int] = Body(...),
                            user_data=Depends(verify_token),
                            db: Session = Depends(get_db)):
    count = await admin_service.update_permission(db=db, admin_id=admin_id, permission_ids=permission_ids)
    if count > 0:
        return BaseResponse(data=count)
    else:
        return BaseError(msg='操作失败！')


'''
@ApiOperation("获取用户所有权限（包括+-权限）")
    @RequestMapping(value = "/permission/{adminId}", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<List<UmsPermission>> getPermissionList(@PathVariable Long adminId) {
        List<UmsPermission> permissionList = adminService.getPermissionList(adminId);
        return CommonResult.success(permissionList);
    }
'''


@ums_admin_router.get('/permission/{adminId}', summary='获取用户所有权限（包括+-权限）')
async def get_permissions(admin_id: int = Path(..., alias='adminId'), user_data=Depends(verify_token),
                          db: Session = Depends(get_db)):
    permissions = await admin_service.get_permission_list(db=db, admin_id=admin_id)
    return BaseResponse(data=permissions)
