from pydantic import BaseModel, Field, validator
from application.api.response import BaseError
import re

'''
@ApiModelProperty(value = "用户名", required = true)
    @NotEmpty(message = "用户名不能为空")
    private String username;
    @ApiModelProperty(value = "密码", required = true)
    @NotEmpty(message = "密码不能为空")
    private String password;
    @ApiModelProperty(value = "用户头像")
    private String icon;
    @ApiModelProperty(value = "邮箱")
    @Email(message = "邮箱格式不合法")
    private String email;
    @ApiModelProperty(value = "用户昵称")
    private String nickName;
    @ApiModelProperty(value = "备注")
    private String note;
'''

mobile_pattern = "^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$"
pwd_pattern = "(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,20}"
user_name_pattern = "^[a-zA-Z0-9_+.-]+@?[a-zA-Z0-9_-]+\.?[a-zA-Z0-9]+$"
email_pattern = "^[a-zA-Z0-9_+.-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9.]+$"


class UmsAdminLoginSchema(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

    @validator('username')
    def validator_username(cls, username):
        username = username.strip()
        if not username or len(username) == 0:
            raise BaseError('用户名不能为空')
        return username

    @validator('password')
    def validator_password(cls, password: str):
        password = password.strip()
        # if not password or len(password) < 6:
        if not password:
            raise BaseError('密码不能为空')
        return password


class UmsAdminInSchema(UmsAdminLoginSchema):
    email: str = Field(..., description="邮箱")
    icon: str = Field(None, description="用户头像")
    nick_name: str = Field(None, alias='nickName', description="用户昵称")
    note: str = Field(None, description="备注")
    status: int = Field(None, description="状态")

    @validator('email')
    def validator_email(cls, email: str):
        email = email.strip()
        if not email or len(email) == 0:
            raise BaseError('邮箱不能为空')
        if not re.match(email_pattern, email):
            raise BaseError('邮箱格式不合法')
        return email


class UmsAdminUpdateSchema(BaseModel):
    username: str = Field(None, description="用户名")
    password: str = Field(None, description="密码")
    email: str = Field(None, description="邮箱")
    icon: str = Field(None, description="用户头像")
    nickName: str = Field(None, description="用户昵称")


class UpdateAdminPasswordSchema(BaseModel):
    username: str = Field(None, description="用户名")
    old_password: str = Field(..., description='旧密码', alias='oldPassword')
    new_password: str = Field(..., description='新密码', alias='newPassword')


class UmsAdminOutSchema(BaseModel):
    pass
