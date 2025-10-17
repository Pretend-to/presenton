from pydantic import BaseModel
from typing import Optional, Any
class R(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
    
    @classmethod
    def success(cls,message: str, data: Any = None) -> "R":
        return cls(code=0, message=message, data=data)
    
    @classmethod
    def error(cls,message: str, data: Any = None) -> "R":
        return cls(code=1, message=message, data=data)