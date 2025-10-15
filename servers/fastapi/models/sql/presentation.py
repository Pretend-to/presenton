from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy import JSON, Column, DateTime, String
from sqlmodel import Boolean, Field, SQLModel

from models.presentation_layout import PresentationLayoutModel
from models.presentation_outline_model import PresentationOutlineModel
from models.presentation_structure_model import PresentationStructureModel
from utils.datetime_utils import get_current_utc_datetime

# PPT主表
class PresentationModel(SQLModel, table=True):
    __tablename__ = "presentations"
    # 主键 uuid，自动生成
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    # 演示内容
    content: str
    # 幻灯片数量
    n_slides: int
    # 语言
    language: str
    # 标题可选
    title: Optional[str] = None
    # 文件路径
    file_paths: Optional[List[str]] = Field(sa_column=Column(JSON), default=None)
    # 大纲
    outlines: Optional[dict] = Field(sa_column=Column(JSON), default=None)
    # 创建时间
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), nullable=False, default=get_current_utc_datetime
        ),
    )
    # 更新时间
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=get_current_utc_datetime,
            onupdate=get_current_utc_datetime,
        ),
    )
    # 布局
    layout: Optional[dict] = Field(sa_column=Column(JSON), default=None)
    # 结构
    structure: Optional[dict] = Field(sa_column=Column(JSON), default=None)
    # 指令
    instructions: Optional[str] = Field(sa_column=Column(String), default=None)
    # 语气
    tone: Optional[str] = Field(sa_column=Column(String), default=None)
    # 冗长程度
    verbosity: Optional[str] = Field(sa_column=Column(String), default=None)
    # 是否包含目录
    include_table_of_contents: bool = Field(sa_column=Column(Boolean), default=False)
    # 是否包含标题幻灯片
    include_title_slide: bool = Field(sa_column=Column(Boolean), default=True)
    # 是否启用网络搜索
    web_search: bool = Field(sa_column=Column(Boolean), default=False)

    def get_new_presentation(self):
        return PresentationModel(
            id=uuid.uuid4(),
            content=self.content,
            n_slides=self.n_slides,
            language=self.language,
            title=self.title,
            file_paths=self.file_paths,
            outlines=self.outlines,
            layout=self.layout,
            structure=self.structure,
            instructions=self.instructions,
            tone=self.tone,
            verbosity=self.verbosity,
            include_table_of_contents=self.include_table_of_contents,
            include_title_slide=self.include_title_slide,
        )

    def get_presentation_outline(self):
        if not self.outlines:
            return None
        return PresentationOutlineModel(**self.outlines)

    def get_layout(self):
        return PresentationLayoutModel(**self.layout)

    def set_layout(self, layout: PresentationLayoutModel):
        self.layout = layout.model_dump()

    def get_structure(self):
        if not self.structure:
            return None
        return PresentationStructureModel(**self.structure)

    def set_structure(self, structure: PresentationStructureModel):
        self.structure = structure.model_dump()
