from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.lifespan import app_lifespan
from api.middlewares import UserConfigEnvUpdateMiddleware
from api.v1.ppt.router import API_V1_PPT_ROUTER
from api.v1.webhook.router import API_V1_WEBHOOK_ROUTER
from api.v1.mock.router import API_V1_MOCK_ROUTER
from api.v1.education.router import API_V1_EDUCATION_ROUTER
from dotenv import load_dotenv
load_dotenv()

# 创建FastAPI应用实例，绑定生命周期管理器
app = FastAPI(lifespan=app_lifespan)


# Routers
app.include_router(API_V1_PPT_ROUTER) # PPT生成相关接口(/api/v1/ppt)
app.include_router(API_V1_WEBHOOK_ROUTER) #Webhook管理接口 (/api/v1/webhook)
app.include_router(API_V1_MOCK_ROUTER) #Mock接口 (/api/v1/mock)
app.include_router(API_V1_EDUCATION_ROUTER) #教育相关接口 (/api/ppt)
# Middlewares
origins = ["*"]
# CORS跨域中间件，允许所有来源的请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允许所有域名访问
    allow_credentials=True,   # 允许发送认证信息
    allow_methods=["*"],      # 允许所有HTTP方法
    allow_headers=["*"],      # 允许所有请求头
)
# 用户配置更新中间件
app.add_middleware(UserConfigEnvUpdateMiddleware)
