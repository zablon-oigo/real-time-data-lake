import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostBase(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None


class PostCreate(PostBase):
    title: str  


class PostUpdate(PostBase):
    pass  

class PostResponse(BaseModel):
    uid: uuid.UUID
    title: str
    body: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
