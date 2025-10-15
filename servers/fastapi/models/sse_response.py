import json

from pydantic import BaseModel

# SSE响应模型
class SSEResponse(BaseModel):
    event: str
    data: str
    def to_string(self):
        return f"event: {self.event}\ndata: {self.data}\n\n"

# SSE状态响应
class SSEStatusResponse(BaseModel):
    status: str

    def to_string(self):
        return SSEResponse(
            event="response", data=json.dumps({"type": "status", "status": self.status})
        ).to_string()

# SSE错误响应
class SSEErrorResponse(BaseModel):
    detail: str

    def to_string(self):
        return SSEResponse(
            event="response", data=json.dumps({"type": "error", "detail": self.detail})
        ).to_string()

# SSE完成响应
class SSECompleteResponse(BaseModel):
    key: str
    value: object

    def to_string(self):
        return SSEResponse(
            event="response",
            data=json.dumps({"type": "complete", self.key: self.value}),
        ).to_string()
