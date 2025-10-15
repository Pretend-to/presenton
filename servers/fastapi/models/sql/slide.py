from typing import Optional
import uuid
from sqlalchemy import ForeignKey
from sqlmodel import Field, Column, JSON, SQLModel

# 幻灯片表
class SlideModel(SQLModel, table=True):
    __tablename__ = "slides"
    # 主键 uuid，自动生成
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    # 外键，关联到ppt表
    presentation: uuid.UUID = Field(
        sa_column=Column(ForeignKey("presentations.id", ondelete="CASCADE"), index=True)
    )
    # 布局组
    layout_group: str
    # 布局
    layout: str
    # 索引
    index: int
    # 内容
    content: dict = Field(sa_column=Column(JSON))
    # html内容
    html_content: Optional[str]
    # 演讲者备注
    speaker_note: Optional[str] = None
    properties: Optional[dict] = Field(sa_column=Column(JSON))

    def get_new_slide(self, presentation: uuid.UUID, content: Optional[dict] = None):
        return SlideModel(
            id=uuid.uuid4(),
            presentation=presentation,
            layout_group=self.layout_group,
            layout=self.layout,
            index=self.index,
            speaker_note=self.speaker_note,
            content=content or self.content,
            properties=self.properties,
        )
