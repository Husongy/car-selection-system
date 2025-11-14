"""
认证API路由 - 登录、注册、获取当前用户信息
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_async_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.response import Response

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=Response[UserResponse], summary="用户注册")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    用户注册
    
    - **username**: 用户名（3-50个字符）
    - **password**: 密码（至少6个字符）
    - **email**: 邮箱（可选）
    """
    # 检查用户名是否已存在
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if user_data.email:
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_email = result.scalar_one_or_none()
        
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
    
    # 创建新用户
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
        is_superuser=False
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return Response(
        code=200,
        message="注册成功",
        data=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=Response[Token], summary="用户登录")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_async_db)
):
    """
    用户登录
    
    - **username**: 用户名
    - **password**: 密码
    
    返回JWT访问令牌
    """
    # 查询用户
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    user = result.scalar_one_or_none()
    
    # 验证用户和密码
    if not user or not verify_password(user_data.password, user.hashed_password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否激活
    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})
    
    return Response(
        code=200,
        message="登录成功",
        data=Token(access_token=access_token, token_type="bearer")
    )


@router.get("/me", response_model=Response[UserResponse], summary="获取当前用户信息")
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前登录用户信息
    
    需要在请求头中携带有效的JWT token
    """
    return Response(
        code=200,
        message="success",
        data=UserResponse.model_validate(current_user)
    )


@router.post("/logout", summary="退出登录")
async def logout():
    """
    退出登录
    
    客户端应删除本地存储的token
    """
    return Response(
        code=200,
        message="退出登录成功",
        data=None
    )
