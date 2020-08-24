from application.service.ums_member_level_service import UmsMemberLevelService
from fastapi import APIRouter, Depends, Query
from application.api.response import BaseError, BaseResponse
from application.authentication.UsernamePasswordAuthenticationToken import verify_token
from application.model import get_db

member_service = UmsMemberLevelService()
ums_member_router = APIRouter()


@ums_member_router.get('/list', summary='查询所有会员等级')
async def member_list(default_status: int = Query(..., alias='defaultStatus'), db=Depends(get_db),
                      user_data=Depends(verify_token)):
    members_list = await member_service.member_list(db, default_status)
    return BaseResponse(data=members_list)
