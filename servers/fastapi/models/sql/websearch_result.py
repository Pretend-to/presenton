from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import JSON, Column, DateTime, String, Integer, Boolean
from sqlmodel import Field, SQLModel, desc
from utils.datetime_utils import get_current_utc_datetime

# 网络检索结果表
class WebSearchResultModel(SQLModel, table=True):
    __tablename__ = "web_search_results"
    
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    session_id: uuid.UUID = Field(foreign_key="ppt_create_sessions.id", index=True,description="关联会话ID")
    
    # 搜索结果
    title: str = Field(description="搜索结果标题")
    content: str = Field(description="搜索结果内容")
    url: str = Field(description="来源URL")
    snippet: str = Field(description="摘要")
    
    # 用户选择
    is_selected: bool = Field(default=True, description="是否被选择使用")
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, default=get_current_utc_datetime
        ),description="创建时间"
    )