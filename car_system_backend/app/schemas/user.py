"""
用户相关Schemas
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., description="用户名", min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None, description="邮箱")


class UserCreate(UserBase):
    """用户注册模型"""
    password: str = Field(..., description="密码", min_length=6, max_length=50)


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserInDB(UserBase):
    """数据库用户模型"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool
    is_superuser: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token响应模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token数据模型"""
    username: Optional[str] = None
