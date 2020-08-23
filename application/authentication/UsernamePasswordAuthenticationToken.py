from fastapi import HTTPException, Depends, status
import jwt
from application.api.response import BaseError
from application.settings import SECRET_KEY, ALGORITHM, jwt_options, error_code
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from application.service.ums_admin_cache_service import UmsAdminCacheService
from application.settings import tokenUrl
from application.model.ums_admin import UmsAdmin
from application.model import get_db
from application.util.token_util import parser_token
from pydantic import BaseModel


class UserData(BaseModel):
    username: str
    user_id: int


validate_credentials_code = error_code

admin_cache_service = UmsAdminCacheService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)
credentials_exception = BaseError(
    status_code=status.HTTP_401_UNAUTHORIZED,
    msg="Could not validate credentials",
    code=validate_credentials_code,
)


# token验证
async def verify_token(token: str = Depends(oauth2_scheme)):
    print("token:{}".format(token))
    if 'Bearer' in token:
        token = token.split(' ')[-1]
    user_data = None
    try:
        user_data = parser_token(token)
        session = admin_cache_service.get_access_token_by_user(username=user_data['username'],
                                                               user_id=user_data['user_id'])
        # 与本地不一致
        if not session or session != token:
            raise credentials_exception
        if user_data['username'] is None:
            raise credentials_exception
    except Exception as e:
        raise credentials_exception
    return UserData(**user_data)


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    user_data = await verify_token(token)
    if not user_data:
        raise credentials_exception
    ums_admin = db.query(UmsAdmin).filter_by(username=user_data.username).first()
    if ums_admin is None:
        raise credentials_exception
    if not ums_admin.status:
        raise BaseError(msg='该用户已被禁用')
    return ums_admin
