from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import JSON, Column, DateTime, String, Integer, Boolean
from sqlmodel import Field, SQLModel, desc
from utils.datetime_utils import get_current_utc_datetime
from models.teaching_objective_item import TeachingObjectiveItem

# 教学目标表
class TeachingObjectiveModel(SQLModel, table=True):
    __tablename__ = "teaching_objectives"
    
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    session_id: uuid.UUID = Field(foreign_key="ppt_create_sessions.id", description="关联会话ID")
    
    # 目标内容
    teaching_objectives: Optional[List[TeachingObjectiveItem]] = Field(
        sa_column=Column(JSON), 
        default_factory=list,
        description="教学目标列表"
    )
    
    
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
    def add_objective(self, content: str) -> TeachingObjectiveItem:
        """添加教学目标"""
        if not self.teaching_objectives:
            self.teaching_objectives = []
        
        new_index = len(self.teaching_objectives) + 1
        objective = TeachingObjectiveItem(content=content, index=new_index)
        self.teaching_objectives.append(objective)
        return objective
    
    def update_objectives(self, objectives: List[TeachingObjectiveItem]):
        """批量更新教学目标"""
        # 重新排序
        for i, obj in enumerate(objectives):
            obj.index = i + 1
        self.teaching_objectives = objectives
    
    def get_objectives_by_index(self, index: int) -> Optional[TeachingObjectiveItem]:
        """按索引获取目标"""
        if not self.teaching_objectives:
            return None
        
        for obj in self.teaching_objectives:
            if obj.index == index:
                return obj
        return None