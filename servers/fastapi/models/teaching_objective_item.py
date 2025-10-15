from pydantic import BaseModel

# 教学目标项
class TeachingObjectiveItem(BaseModel):
    content: str
    index: int
    