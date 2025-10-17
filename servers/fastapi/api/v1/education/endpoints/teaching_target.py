from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List
import uuid
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_create_sessions import PptCreateSessionModel
from models.common.R import R
from enums.ppt_session import PptSessionState
from sqlmodel import select

EDUCATION_TEACHING_TARGET_ROUTER = APIRouter(prefix="")

class ConfirmTargetRequest(BaseModel):
    sessionId: uuid.UUID
    target: List[str]

def mock_target():
    return [
        "掌握双曲线的定义、标准方程和几何性质",
        "理解双曲线的焦点、准线及其几何意义",
        "能够利用双曲线的性质解决相关问题",
    ]
@EDUCATION_TEACHING_TARGET_ROUTER.get("/generate/target", response_model=R)
async def get_teaching_target(
    s: uuid.UUID = Query(..., description="会话ID"),
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    获取教学目标
    """
    try:
        # 根据sessionId查询会话记录
        result = await sql_session.execute(
            select(PptCreateSessionModel).where(PptCreateSessionModel.sessionId == s)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            return R.error("会话不存在")
        
        if session.target is None or len(session.target) == 0:
            session.target = mock_target()
        # 返回教学目标列表
        return R.success("获取成功", session.target)
        
    except Exception as e:
        return R.error("获取教学目标失败", str(e))


@EDUCATION_TEACHING_TARGET_ROUTER.post("/generate/target", response_model=R)
async def confirm_teaching_target(
    request: ConfirmTargetRequest = Body(...),
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    确认教学目标
    """
    try:
        # 根据sessionId查询会话记录
        result = await sql_session.execute(
            select(PptCreateSessionModel).where(PptCreateSessionModel.sessionId == request.sessionId)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            return R.error("会话不存在")
        
        # 更新教学目标和会话状态
        session.target = request.target
        #session.state = PptSessionState.COMFIRMTARGET
        
        # 保存更改
        sql_session.add(session)
        await sql_session.commit()
        
        return R.success("success")
        
    except Exception as e:
        await sql_session.rollback()
        return R.error("确认教学目标失败", str(e))
