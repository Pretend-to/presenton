from datetime import datetime
from typing import Any, List, Optional,Dict
import uuid
from sqlalchemy import JSON, Column, DateTime, String, Integer, Boolean
from sqlmodel import Field, SQLModel, desc
from utils.datetime_utils import get_current_utc_datetime
from enums.ppt_session import PptSessionState,ClassType
# PPT创建会话表
class PptCreateSessionModel(SQLModel, table=True):
    __tablename__ = "ppt_create_sessions"
    
    # 基础字段
    sessionId: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    userId: str = Field(index=True,description="用户ID")
    userInput: str = Field(description="用户输入的查询")
    title: str = Field(description="LLM总结标题")
    # 配置信息
    pages: int = Field(description="页数")
    classType: ClassType = Field(default=ClassType.NEW_LESSON, description="课程类别: 新授课 | 复习课") 
    kbIds: List[str] = Field(sa_column=Column(JSON),description="知识库ID列表")
    webSearch: bool = Field(default=False, description="是否开启网络搜索")
    
    webSearchContent: str = Field(description="网络搜索内容",default="")
    # 状态管理
    state: PptSessionState = Field(default=PptSessionState.COMFIRMFILES, description="会话状态 'confirmFiles' | 'confirmTarget' | 'confirmOutline' | 'generatePPT' | 'completeGeneration'")
    # 教学目标
    target: List[str] = Field(sa_column=Column(JSON),description="教学目标",default=[])
    # 教学大纲
    outline: Dict[str, Any] = Field(
        default_factory=dict,  # 使用 default_factory 避免可变默认参数问题
        sa_column=Column(JSON), 
        description="教学大纲 (JSON格式)"
    )
    # 教学设计
    design: str = Field(description="教学设计",default="")
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