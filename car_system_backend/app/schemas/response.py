"""
通用响应Schemas
"""
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List

DataT = TypeVar('DataT')


class Response(BaseModel, Generic[DataT]):
    """统一响应模型"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: Optional[DataT] = Field(None, description="响应数据")


class PageResponse(BaseModel, Generic[DataT]):
    """分页响应模型"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: List[DataT] = Field([], description="数据列表")
    total: int = Field(0, description="总数")
    page: int = Field(1, description="当前页")
    page_size: int = Field(10, description="每页数量")
