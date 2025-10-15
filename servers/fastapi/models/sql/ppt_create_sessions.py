from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import JSON, Column, DateTime, String, Integer, Boolean
from sqlmodel import Field, SQLModel, desc
from utils.datetime_utils import get_current_utc_datetime

# PPT创建会话表
class PptCreateSessionModel(SQLModel, table=True):
    __tablename__ = "ppt_create_sessions"
    
    # 基础字段
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: str = Field(index=True,description="用户ID")
    query: str = Field(description="用户输入的主题")
    
    # 配置信息
    pages: int = Field(description="页数")
    classtype: int = Field(description="课程类别: 0: 新授课 1:复习课") 
    documents: Optional[List[str]] = Field(sa_column=Column(JSON), default=None, description="参考文档路径列表")
    knowledge_base_type: int = Field(description="知识库类型：0: 班级空间 1:团队空间 2:创造空间")
    websearch_enabled: bool = Field(default=False, description="是否开启网络搜索")
    
    # 状态管理
    current_step: int = Field(default=0, description="当前步骤: 0: 创建 1: 生成 2: 完成")
    #status: str = Field(default="active", description="会话状态")
    
    # 创建时间
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, default=get_current_utc_datetime,index=True
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
    
    # 关联的演示文稿ID（最终生成后填入）
    presentation_id: Optional[uuid.UUID] = Field(default=None,index=True, description="关联的演示文稿ID")