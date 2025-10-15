from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import JSON, Column, DateTime, String, Integer, Boolean
from sqlmodel import Field, SQLModel, desc
from utils.datetime_utils import get_current_utc_datetime

# 知识召回表
class KnowledgeRecallModel(SQLModel, table=True):
    __tablename__ = "knowledge_recalls"
    
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    session_id: uuid.UUID = Field(foreign_key="ppt_create_sessions.id", index=True,description="关联会话ID")
    
    # 召回内容
    content: str = Field(description="召回的文本内容")
    source: str = Field(description="召回来源")
    score: float = Field(index=True,description="相关性评分")
    chunk_id: str = Field(description="文档块ID")
    
    # 用户选择状态
    is_selected: bool = Field(default=False, index=True, description="用户是否选择该片段")
    selected_at: Optional[datetime] = Field(default=None, description="选择时间")
    
    # 元数据
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, default=get_current_utc_datetime
        ),description="创建时间"
    )