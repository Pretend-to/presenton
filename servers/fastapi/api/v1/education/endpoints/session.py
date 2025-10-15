from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import uuid
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_create_sessions import PptCreateSessionModel
from utils.datetime_utils import get_current_utc_datetime
EDUCATION_SESSION_ROUTER = APIRouter(prefix="/session")

class CreateSessionRequest(BaseModel):
    user_id: str
    query: str
    pages: int
    classtype: int
    documents: Optional[List[str]] = None
    knowledge_base_type: int  # 0: 班级空间 1:团队空间 2:创造空间
    websearch_enabled: bool = False

class SessionResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    query: str
    current_step: int
    # ... 其他字段

@EDUCATION_SESSION_ROUTER.post("/create", response_model=SessionResponse)
async def create_education_session(
    request: CreateSessionRequest,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    创建PPT生成会话
    """
    session = PptCreateSessionModel(
        user_id=request.user_id,
        query=request.query,
        pages=request.pages,
        classtype=request.classtype,
        documents=request.documents,
        knowledge_base_type=request.knowledge_base_type,
        websearch_enabled=request.websearch_enabled,
        current_step=0
    )
    
    sql_session.add(session)
    await sql_session.commit()
    
    return SessionResponse(**session.model_dump())

@EDUCATION_SESSION_ROUTER.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: uuid.UUID,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """获取会话信息"""
    session = await sql_session.get(PptCreateSessionModel, session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return SessionResponse(**session.model_dump())

@EDUCATION_SESSION_ROUTER.patch("/{session_id}/step")
async def update_session_step(
    session_id: uuid.UUID,
    step: int = Body(..., embed=True),
    sql_session: AsyncSession = Depends(get_async_session)
):
    """更新会话步骤"""
    session = await sql_session.get(PptCreateSessionModel, session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    session.current_step = step
    await sql_session.commit()
    
    return {"success": True, "current_step": step}