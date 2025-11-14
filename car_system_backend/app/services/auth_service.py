"""
认证服务层 - 处理用户认证业务逻辑
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import Optional

from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    """认证服务类"""
    
    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """
        验证用户凭据
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            验证成功返回User对象，失败返回None
        """
        try:
            # 查询用户
            result = await db.execute(
                select(User).where(User.username == username)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            # 验证密码
            if not verify_password(password, str(user.hashed_password)):
                return None
            
            return user
            
        except Exception as e:
            print(f"用户验证错误: {e}")
            return None
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
        """
        创建新用户
        
        Args:
            db: 数据库会话
            user_data: 用户创建数据
            
        Returns:
            创建的用户对象
            
        Raises:
            HTTPException: 用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        result = await db.execute(
            select(User).where(User.username == user_data.username)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if user_data.email:
            result = await db.execute(
                select(User).where(User.email == user_data.email)
            )
            if result.scalar_one_or_none():
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
        
        return new_user
    
    @staticmethod
    def generate_token(user: User) -> str:
        """
        为用户生成JWT token
        
        Args:
            user: 用户对象
            
        Returns:
            JWT token字符串
        """
        return create_access_token(data={"sub": user.username})
