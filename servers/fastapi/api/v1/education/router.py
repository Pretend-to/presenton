from fastapi import APIRouter

from api.v1.education.endpoints.session import EDUCATION_SESSION_ROUTER
from api.v1.education.endpoints.knowledge import KNOWLEDGE_ROUTER
API_V1_EDUCATION_ROUTER = APIRouter(prefix="/api/v1/edu", tags=["Education"])

API_V1_EDUCATION_ROUTER.include_router(EDUCATION_SESSION_ROUTER)
API_V1_EDUCATION_ROUTER.include_router(KNOWLEDGE_ROUTER)