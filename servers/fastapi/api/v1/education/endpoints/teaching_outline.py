from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_create_sessions import PptCreateSessionModel
from models.common.R import R
from enums.ppt_session import PptSessionState
from sqlmodel import select

EDUCATION_TEACHING_OUTLINE_ROUTER = APIRouter(prefix="")

class OutlineNode(BaseModel):
    title: str
    children: List[OutlineNode] = []

class ConfirmOutlineRequest(BaseModel):
    sessionId: uuid.UUID
    tree: OutlineNode

def mock_outline():
    return {"title": "AI大模型应用", "children": [{"title": "课程导学与职业发展", "children": [{"title": "你将收获哪些能力", "children": []}, {"title": "AI时代需要什么样的人才", "children": []}, {"title": "职业发展路径规划", "children": []}]}, {"title": "初识AI大模型与提示词工程", "children": [{"title": "提示词工程最佳实践", "children": []}]}, {"title": "AI核心技术与模型", "children": [{"title": "主流大模型(GPT/Claude)解析", "children": []}]}]}
@EDUCATION_TEACHING_OUTLINE_ROUTER.get("/generate/outline", response_model=R)
async def get_teaching_outline(
    s: uuid.UUID = Query(..., description="会话ID"),
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    获取教学活动设计
    """
    try:
        # 根据sessionId查询会话记录
        result = await sql_session.execute(
            select(PptCreateSessionModel).where(PptCreateSessionModel.sessionId == s)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            return R.error("会话不存在")
        
        # 如果outline为空，返回默认结构
        if session.outline is None or len(session.outline) == 0:
            default_outline = mock_outline()
            return R.success("success", default_outline)
        
        # 返回教学大纲
        return R.success("success", session.outline)
        
    except Exception as e:
        return R.error("获取教学活动设计失败", str(e))


@EDUCATION_TEACHING_OUTLINE_ROUTER.post("/generate/outline", response_model=R)
async def confirm_teaching_outline(
    request: ConfirmOutlineRequest = Body(...),
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    确认教学活动设计
    """
    try:
        # 根据sessionId查询会话记录
        result = await sql_session.execute(
            select(PptCreateSessionModel).where(PptCreateSessionModel.sessionId == request.sessionId)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            return R.error("会话不存在")
        
        # 将tree转换为dict格式存储
        outline_dict = request.tree.model_dump()
        
        # 更新教学大纲
        session.outline = outline_dict
        
        # 保存更改
        sql_session.add(session)
        await sql_session.commit()
        
        return R.success("success")
        
    except Exception as e:
        await sql_session.rollback()
        return R.error("确认教学活动设计失败", str(e))
