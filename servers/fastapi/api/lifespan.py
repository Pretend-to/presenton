from contextlib import asynccontextmanager
import os

from fastapi import FastAPI

from services.database import create_db_and_tables
from utils.get_env import get_app_data_directory_env
from utils.model_availability import (
    check_llm_and_image_provider_api_or_model_availability,
)


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Initializes the application data directory and checks LLM model availability.
    Fastapi生命周期管理
    """
    os.makedirs(get_app_data_directory_env(), exist_ok=True)  # 创建应用数据目录
    await create_db_and_tables()  # 创建数据库表
    await check_llm_and_image_provider_api_or_model_availability()  # 检查LLM模型和图片提供者API的可用性
    yield
