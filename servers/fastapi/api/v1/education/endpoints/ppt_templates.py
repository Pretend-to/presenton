from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
import uuid
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_template import PptTemplateModel
from models.common.R import R
from sqlmodel import select

EDUCATION_PPT_TEMPLATES_ROUTER = APIRouter(prefix="")

class TemplateItem(BaseModel):
    id: uuid.UUID
    title: str
    cover: str

def mock_templates():
    return [
    {
      "id": "e9a3b2c1-8d7e-4f6a-9b8c-7d6e5f4a3b2c",
      "title": "商务简约蓝",
      "cover": "https://via.placeholder.com/800x600.png/007BFF/FFFFFF?text=Business"
    },
    {
      "id": "f0c3d4e5-a6b7-4c8d-9e0f-1a2b3c4d5e6f",
      "title": "教育卡通风",
      "cover": "https://via.placeholder.com/800x600.png/28A745/FFFFFF?text=Education"
    },
    {
      "id": "12345678-90ab-cdef-1234-567890abcdef",
      "title": "科技未来感",
      "cover": "https://via.placeholder.com/800x600.png/17A2B8/FFFFFF?text=Technology"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "清新文艺绿",
      "cover": "https://via.placeholder.com/800x600.png/4CAF50/FFFFFF?text=Fresh"
    },
    {
      "id": "c4e2a1b3-6d5e-4f7a-8b9c-0d1e2f3a4b5c",
      "title": "中国风水墨",
      "cover": "https://via.placeholder.com/800x600.png/DC3545/FFFFFF?text=Tradition"
    }
  ]
@EDUCATION_PPT_TEMPLATES_ROUTER.get("/templates", response_model=R)
async def get_ppt_templates(
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    获取模板列表
    """
    try:
        # 查询所有模板记录
        result = await sql_session.execute(
            select(PptTemplateModel).order_by(PptTemplateModel.created_at.desc())
        )
        templates = result.scalars().all()
        
        # 转换为响应格式
        if templates is None or len(templates) == 0:
            return R.success("success", data=mock_templates())

        return R.success("success", data=templates)
        
    except Exception as e:
        return R.error("获取模板列表失败", str(e))
