from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import JSON, Column, DateTime, ForeignKey
from sqlmodel import Field, SQLModel
from utils.datetime_utils import get_current_utc_datetime

# 教学设计表
class TeachingDesignModel(SQLModel, table=True):
    __tablename__ = "teaching_designs"
    
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    session_id: uuid.UUID = Field(foreign_key="ppt_create_sessions.id", description="关联会话ID")
    
    # 教学设计各部分
    design_content: str = Field(description="教学设计内容")
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, default=get_current_utc_datetime
        ),description="创建时间"
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=get_current_utc_datetime,
            onupdate=get_current_utc_datetime,
        ),description="更新时间"
    )