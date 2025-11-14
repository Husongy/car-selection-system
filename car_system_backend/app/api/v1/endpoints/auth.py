"""
认证API路由 - 登录、注册、获取当前用户信息
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.response import Response
from app.services.auth_service import AuthService

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
    try:
        # 创建用户
        new_user = await AuthService.create_user(db, user_data)
        
        return Response(
            code=200,
            message="注册成功",
            data=UserResponse.model_validate(new_user)
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"注册错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败，请稍后重试"
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
    try:
        # 验证用户
        user = await AuthService.authenticate_user(
            db,
            user_data.username,
            user_data.password
        )
        
        if not user:
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
        
        # 生成token
        access_token = AuthService.generate_token(user)
        
        return Response(
            code=200,
            message="登录成功",
            data=Token(access_token=access_token, token_type="bearer")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"登录错误: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
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
