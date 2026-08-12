from pydantic import BaseModel, Field
from datetime import datetime

class UserRequest(BaseModel):
    username: str
    password: str


# user_info 基础类型
class UserInfoBase(BaseModel):
    nickname: str | None = Field(None, max_length=50, description='昵称')
    avatar: str | None = Field(None, max_length=255, description='头像')
    gender: str | None = Field(None, max_length=10, description='性别')
    phone: str | None = Field(None, max_length=20, description='手机号')
    bio: str | None = Field(None, max_length=255, description='个人介绍')

# user_info 对应的类
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = {
        'from_attributes': True, # 允许从模型属性中获取值
    }


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias='userInfo', description='用户信息')

    model_config = {
        'from_attributes': True, # 允许从模型属性中获取值
        'populate_by_name': True, # 允许alias 根据字段名填充值
    }