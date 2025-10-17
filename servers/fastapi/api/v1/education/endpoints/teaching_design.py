# 在现有的导入部分添加以下导入
from fastapi import APIRouter, Depends, HTTPException, Body, Query
from fastapi.responses import StreamingResponse
import json
import asyncio
from pydantic import BaseModel
from typing import Optional
from services.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.sql.ppt_create_sessions import PptCreateSessionModel
import uuid
from sqlmodel import select, delete

EDUCATION_TEACHING_DESIGN_ROUTER = APIRouter(prefix="")

# 在现有的响应模型后添加SSE响应模型
class SSEFrame(BaseModel):
    type: str  # "pending" | "streaming" | "finish"| "error"
    chunk: Optional[str] = None
    msg: Optional[str] = None

def mock_design():
    return """
好的，这是使用简体中文为您准备的二次函数课程教学计划。

---

### **二次函数课程教学计划**

#### ** 教学目标**

1.  **知识与理解 (Knowledge & Understanding):**
    * 学生能够识别二次函数 ($y = ax^2 + bx + c$, 其中 $a \neq 0$) 的标准形式、顶点形式和截距形式，并理解参数 $a$、$b$、$c$ 如何影响其抛物线图像的开口方向、宽度和位置。

2.  **技能与应用 (Skills & Application):**
    * 学生能够熟练运用配方法或公式法找出二次函数的顶点坐标、对称轴方程，并能计算出图像与 $x$ 轴和 $y$ 轴的交点（如果存在）。

3.  **分析与解决问题 (Analysis & Problem-Solving):**
    * 学生能够将现实世界中的问题（例如：最大利润、最小成本、抛物体运动轨迹）抽象为二次函数模型，并利用二次函数的性质（特别是最大值或最小值）来解决这些实际问题。

#### ** 教学重难点**

* **教学重点 (Key Points):**
    1.  **图像与性质的连接：** 掌握二次函数的图像（抛物线）及其核心性质，包括开口方向、顶点、对称轴，并能将这些性质与函数表达式中的参数 ($a, h, k$) 建立直接联系。
    2.  **顶点的求解与应用：** 熟练掌握求顶点坐标的方法（尤其是配方法），并理解顶点在解决最大值与最小值问题中的关键作用。
    3.  **数形结合思想：** 运用图像来直观理解代数问题（如一元二次方程的根对应图像与 $x$ 轴的交点），也运用代数计算来精确分析图像的性质。

* **教学难点 (Difficult Points):**
    1.  **配方法的代数操作：** “配方法”涉及较为繁琐的代数变形，对学生的计算能力要求较高，容易出错。
    2.  **建立数学模型：** 将实际应用题的文字描述转化为二次函数的数学模型，是从理论到实践的关键一步，需要较强的抽象思维能力。
    3.  **参数的综合影响：** 理解标准式 $y = ax^2 + bx + c$ 中，参数 $b$ 和 $c$ 如何共同影响图像的平移，比理解顶点式中的 $h, k$ 更加抽象。

#### ** 教学过程**

本课程将遵循“从具体到抽象，从基础到应用”的原则，引导学生逐步掌握二次函数的核心概念。

1.  **引入与基础探索 (从 `y = ax²` 开始):**
    * 从生活中的抛物线实例（如投篮轨迹、拱桥）引入，激发学生兴趣。
    * 首先研究最简单的二次函数 `y = ax²`，通过描点绘图，让学生直观感受参数 `a` 如何决定开口方向（正上负下）与开口大小（绝对值越大越窄）。

2.  **平移与顶点式 (学习 `y = a(x-h)² + k`):**
    * 在 `y = ax²` 的基础上，探讨图像的上下平移（`+k`）与左右平移（`-h`），自然地引出**顶点式 `y = a(x-h)² + k`**。
    * 强调顶点 `(h, k)` 和对称轴 `x = h` 是图像的关键，让学生学会从顶点式中直接读出这些核心信息。

3.  **标准式与配方法 (攻克 `y = ax² + bx + c`):**
    * 介绍最常见的**标准式**，并提出核心问题：“如何从标准式中找到顶点？”
    * 将此问题转化为“如何将标准式变为顶点式”，从而引入**“配方法”**这一关键代数工具。通过分步讲解和大量练习，帮助学生克服此难点。同时，可以推导并介绍顶点公式 $x = -\frac{b}{2a}$ 作为快速验算的方法。

4.  **图像与坐标轴的交点：**
    * 探讨图像与 `y` 轴的交点（令 `x=0`），以及与 `x` 轴的交点（令 `y=0`）。
    * 将求 `x` 轴交点的问题与解**一元二次方程** `ax² + bx + c = 0` 连接起来，并利用判别式 $b^2 - 4ac$ 的正负来判断交点个数，深化“数形结合”的思想。

5.  **实际应用与建模：**
    * 提供利润最大化、面积最大化、运动路径最高点等真实情境的应用题。
    * 引导学生分析题目、设定变量、列出函数关系式，最终将问题转化为求二次函数的**最大值或最小值**（即求顶点的 `y` 坐标）。

6.  **总结与巩固：**
    * 回顾二次函数的三种形式及其优缺点，梳理知识体系。
    * 通过综合性练习，巩固学生绘制图像、求解性质和解决实际问题的能力。
"""
# 在现有接口后添加以下接口
@EDUCATION_TEACHING_DESIGN_ROUTER.get("/generate/target-description")
async def get_teaching_design_description(
    s: uuid.UUID = Query(..., description="会话ID"),
    sql_session: AsyncSession = Depends(get_async_session)
):
    """
    获取教学设计描述 (SSE流式响应)
    """
    async def generate_sse():
        try:
            # 发送pending状态
            pending_frame = SSEFrame(type="pending", msg="正在获取教学设计...")
            yield f"{json.dumps(pending_frame.model_dump(), ensure_ascii=False)}\n\n"
            
            # 查询会话记录
            result = await sql_session.execute(
                select(PptCreateSessionModel).where(PptCreateSessionModel.sessionId == s)
            )
            session = result.scalar_one_or_none()
            
            if not session:
                error_frame = SSEFrame(type="error", msg="会话不存在")
                yield f"{json.dumps(error_frame.model_dump(), ensure_ascii=False)}\n\n"
                return
            
            # 获取教学设计内容
            design_content = session.design or mock_design()
            
            # 模拟流式输出，按字符或单词分块发送
            chunk_size = 10  # 每次发送的字符数
            for i in range(0, len(design_content), chunk_size):
                chunk = design_content[i:i + chunk_size]
                streaming_frame = SSEFrame(type="streaming", chunk=chunk)
                yield f"{json.dumps(streaming_frame.model_dump(), ensure_ascii=False)}\n\n"
                
                # 添加小延迟模拟真实的流式输出
                await asyncio.sleep(0.1)
            
            # 发送结束信号（可选）
            end_frame = SSEFrame(type="finish", chunk="", msg="传输完成")
            yield f"{json.dumps(end_frame.model_dump(), ensure_ascii=False)}\n\n"
            
        except Exception as e:
            error_frame = SSEFrame(type="error", msg=f"获取教学设计失败: {str(e)}")
            yield f"{json.dumps(error_frame.model_dump(), ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )