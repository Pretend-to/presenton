from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import uuid
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_create_sessions import PptCreateSessionModel
from models.sql.ppt_create_reference_files import PptCreateReferenceFilesModel
from models.common.R import R

KNOWLEDGE_BASE_ROUTER = APIRouter(prefix="")

class FileItem(BaseModel):
    name: str
    content: Optional[str] = None
    url: Optional[str] = None

class ConcatFilesRequest(BaseModel):
    sessionId: uuid.UUID
    files: List[FileItem]

@KNOWLEDGE_BASE_ROUTER.post("/generate/concat", response_model=R)
async def concat_reference_files(
    request: ConcatFilesRequest,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    为PPT生成会话追加参考文件
    """
    try:
        # 验证会话是否存在
        session = await sql_session.get(PptCreateSessionModel, request.sessionId)
        if not session:
            return R.error("会话不存在")
        
        # 创建参考文件记录
        # 因为验证已完成，可以直接创建对象
        reference_files = [
            PptCreateReferenceFilesModel(
                sessionId=request.sessionId,
                name=file_item.name,
                content=file_item.content or "",
                url=file_item.url or ""
            ) for file_item in request.files
        ]
        
        # 批量添加到数据库
        sql_session.add_all(reference_files)
        await sql_session.commit()
        
        return R.success("success")
        
    except Exception as e:
        await sql_session.rollback()
        return R.error("添加参考文件失败", str(e))