import uuid
from sqlmodel import Field, SQLModel

# 知识召回表
class PptCreateReferenceFilesModel(SQLModel, table=True):
    __tablename__ = "ppt_create_reference_files"
    
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    sessionId: uuid.UUID = Field(foreign_key="ppt_create_sessions.sessionId", index=True,description="关联会话ID")
    
    name: str = Field(description="文件名称")
    content: str = Field(description="文件内容")
    url: str = Field(description="文件URL")