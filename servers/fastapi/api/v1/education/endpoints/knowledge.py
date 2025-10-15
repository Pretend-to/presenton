from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import uuid
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_create_sessions import PptCreateSessionModel
from utils.datetime_utils import get_current_utc_datetime
from models.sql.knowledge_recall import KnowledgeRecallModel
from sqlmodel import select, update, and_
KNOWLEDGE_ROUTER = APIRouter(prefix="/knowledge")

class KnowledgeRecallItem(BaseModel):
    content: str
    source: str
    score: float
    chunk_id: str

class KnowledgeRecallResponse(BaseModel):
    session_id: uuid.UUID
    recalls: List[KnowledgeRecallItem]
    total_count: int

@KNOWLEDGE_ROUTER.post("/{session_id}/recall", response_model=KnowledgeRecallResponse)
async def trigger_knowledge_recall(
    session_id: uuid.UUID,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    步骤3: 触发知识库召回
    """
    session = await sql_session.get(PptCreateSessionModel, session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    
    # Mock 知识库召回 (实际实现时调用真实的知识库API)
    mock_recalls = [
        {
            "content": f"关于{session.query}的相关知识点1...",
            "source": f"{session.knowledge_base_type}文档1",
            "score": 0.95,
            "chunk_id": "chunk_001"
        },
        {
            "content": f"关于{session.query}的相关知识点2...",
            "source": f"{session.knowledge_base_type}文档2", 
            "score": 0.88,
            "chunk_id": "chunk_002"
        },
        {
            "content": f"关于{session.query}的相关知识点3...",
            "source": f"{session.knowledge_base_type}文档3",
            "score": 0.82,
            "chunk_id": "chunk_003"
        }
    ]
    
    # 保存召回结果到数据库
    recall_models = []
    for recall_data in mock_recalls:
        recall_model = KnowledgeRecallModel(
            session_id=session_id,
            content=recall_data["content"],
            source=recall_data["source"],
            score=recall_data["score"],
            chunk_id=recall_data["chunk_id"]
        )
        recall_models.append(recall_model)
    
    sql_session.add_all(recall_models)
    await sql_session.commit()
    
    return KnowledgeRecallResponse(
        session_id=session_id,
        recalls=[KnowledgeRecallItem(**r) for r in mock_recalls],
        total_count=len(mock_recalls)
    )

class UpdateSelectionRequest(BaseModel):
    session_id: uuid.UUID
    selected_chunk_ids: List[str]

@KNOWLEDGE_ROUTER.post("/{session_id}/selection", response_model=dict)
async def update_knowledge_selection(
    request: UpdateSelectionRequest,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    步骤4: 更新用户选择的知识片段
    """
    # 先取消所有选择
    await sql_session.execute(
        update(KnowledgeRecallModel)
        .where(KnowledgeRecallModel.session_id == request.session_id)
        .values(is_selected=False, selected_at=None)
    )
    
    # 更新选中的片段
    if request.selected_chunk_ids:
        await sql_session.execute(
            update(KnowledgeRecallModel)
            .where(
                and_(
                    KnowledgeRecallModel.session_id == request.session_id,
                    KnowledgeRecallModel.chunk_id.in_(request.selected_chunk_ids)
                )
            )
            .values(is_selected=True, selected_at=get_current_utc_datetime())
        )
    
    await sql_session.commit()
    
    return {
        "success": True,
        "selected_count": len(request.selected_chunk_ids)
    }

@KNOWLEDGE_ROUTER.get("/{session_id}/recalls", response_model=List[KnowledgeRecallItem])
async def get_knowledge_recalls(
    session_id: uuid.UUID,
    sql_session: AsyncSession = Depends(get_async_session)
):
    """获取知识召回结果"""
    recalls = await sql_session.scalars(
        select(KnowledgeRecallModel)
        .where(KnowledgeRecallModel.session_id == session_id)
        .order_by(KnowledgeRecallModel.score.desc())
    )
    
    return [
        KnowledgeRecallItem(
            content=r.content,
            source=r.source, 
            score=r.score,
            chunk_id=r.chunk_id,
            metadata=r.metadata
        ) for r in recalls
    ]