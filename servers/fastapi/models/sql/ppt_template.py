from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel
from utils.datetime_utils import get_current_utc_datetime
from sqlalchemy import Column, DateTime
# ppt模版表
class PptTemplateModel(SQLModel, table=True):
    __tablename__ = "ppt_templates"
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    title: str = Field(description="模板标题")
    cover: str = Field(description="封面图片URL")
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, default=get_current_utc_datetime
        ),
    )
    