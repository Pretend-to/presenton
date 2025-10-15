from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import JSON, Column, DateTime, ForeignKey
from sqlmodel import Field, SQLModel
from utils.datetime_utils import get_current_utc_datetime
class TeachingOutlineModel(SQLModel, table=True):
    __tablename__ = "teaching_outlines"
    
    # --- 基础字段 ---
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    session_id: uuid.UUID = Field(
        foreign_key="ppt_create_sessions.id", 
        index=True,  # 关键索引：用于快速获取某个会话的全部大纲节点
        description="关联会话ID"
    )
    
    # --- 增加父节点ID
    parent_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="teaching_outlines.id", # 这是一个自引用外键
        index=True, # 关键索引：用于快速查找某个节点的所有子节点
        description="父节点ID，如果为None则表示为根节点"
    )
    
    # --- 节点内容信息 ---
    title: str = Field(description="大纲标题")
    # order_index 现在用于决定“兄弟节点”之间的顺序
    order_index: int = Field(default=0, description="在同级节点中的顺序")
    
    
    # 创建时间
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, default=get_current_utc_datetime
        ),description="创建时间"
    )
    # 更新时间
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=get_current_utc_datetime,
            onupdate=get_current_utc_datetime,
        ),description="更新时间"
    )