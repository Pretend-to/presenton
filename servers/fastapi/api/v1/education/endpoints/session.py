from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import uuid
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_create_sessions import PptCreateSessionModel
from models.sql.ppt_create_reference_files import PptCreateReferenceFilesModel
from utils.datetime_utils import get_current_utc_datetime
from enums.ppt_session import ClassType
from models.common.R import R
from sqlmodel import select, delete
from sqlalchemy import and_, desc
from typing import Optional as OptionalType
EDUCATION_SESSION_ROUTER = APIRouter(prefix="")

class SessionConfig(BaseModel):
    pages: int
    classType: ClassType
    kbIds: List[str]
    webSearch: bool

class ChooseFile(BaseModel):
    name: str
    content: str
    url: str
class CreateSessionRequest(BaseModel):
    userId: str
    userInput: str
    config: SessionConfig
    files: List[ChooseFile]

class CreateSessionResponse(BaseModel):
    sessionId: uuid.UUID
    title: str

@EDUCATION_SESSION_ROUTER.post("/generate/init", response_model=R)
async def create_education_session(
    request: CreateSessionRequest,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    创建PPT生成会话
    """
    try:
        session = PptCreateSessionModel(
            userId=request.userId,
            userInput=request.userInput,
            pages=request.config.pages,
            classType=request.config.classType,
            kbIds=request.config.kbIds,
            webSearch=request.config.webSearch,
            title=request.userInput+"PPT生成任务"
        )
        
        sql_session.add(session)
        
        files = [PptCreateReferenceFilesModel(
            sessionId=session.sessionId,
            name=file.name,
            content=file.content,
            url=file.url
        ) for file in request.files]
        sql_session.add_all(files)
        await sql_session.commit()
        return R.success("初始化成功",CreateSessionResponse(sessionId=session.sessionId, title=session.title))
    except Exception as e:
        await sql_session.rollback()
        return R.error("初始化失败",str(e))



# 添加新的响应模型（在现有模型后添加）
class PptHistoryItem(BaseModel):
    sessionId: uuid.UUID
    state: str
    title: str
    created: int  # timestamp

class PptHistoryResponse(BaseModel):
    sessions: List[PptHistoryItem]
    
# 在现有 imports 后添加
from sqlmodel import select, delete
from sqlalchemy import and_, desc
from typing import Optional as OptionalType

# 添加新的响应模型（在现有模型后添加）
class PptHistoryItem(BaseModel):
    sessionId: uuid.UUID
    state: str
    title: str
    created: datetime  # timestamp

class PptHistoryResponse(BaseModel):
    sessions: List[PptHistoryItem]

# 在现有的 create_education_session 接口后添加以下两个接口：

@EDUCATION_SESSION_ROUTER.get("/list", response_model=R)
async def get_ppt_creation_history(
    userId: str,
    title: OptionalType[str] = None,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    获取用户PPT创建历史记录
    """
    try:
        # 构建查询条件
        query = select(PptCreateSessionModel).where(PptCreateSessionModel.userId == userId).order_by(desc(PptCreateSessionModel.created_at))
        
        # 如果提供了title参数，添加模糊查询条件
        if title:
            query = query.where(PptCreateSessionModel.title.contains(title))
        
        # 执行查询
        result = await sql_session.execute(query)
        sessions = result.scalars().all()
        
        # 转换为响应格式
        history_items = []
        for session in sessions:
            history_items.append(PptHistoryItem(
                sessionId=session.sessionId,
                state=session.state.value,  # 枚举值转为字符串
                title=session.title,
                created=session.created_at  # 转换为时间戳
            ))
        
        return R.success("响应成功", history_items)
        
    except Exception as e:
        return R.error("获取历史记录失败", str(e))


@EDUCATION_SESSION_ROUTER.delete("/{session_id}", response_model=R)
async def delete_ppt_session(
    session_id: uuid.UUID,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    删除一条PPT记录
    """
    try:
        # 查找要删除的会话
        session = await sql_session.get(PptCreateSessionModel, session_id)
        
        if not session:
            return R.error("该ppt不存在")
        
        # 先删除关联的参考文件记录
        await sql_session.execute(
            delete(PptCreateReferenceFilesModel).where(
                PptCreateReferenceFilesModel.sessionId == session_id
            )
        )
        
        # 删除会话记录
        await sql_session.delete(session)
        await sql_session.commit()
        
        return R.success("删除成功")
        
    except Exception as e:
        await sql_session.rollback()
        return R.error("删除失败", str(e))