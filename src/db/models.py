from sqlmodel import SQLModel, Field, Column
from sqlalchemy import func
import sqlalchemy.dialects.mysql as my
import uuid
from typing import Optional
from datetime import datetime

class Post(SQLModel, table=True):
    __tablename__ = "post"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(my.CHAR(36), primary_key=True, nullable=False)
    )

    title: str
    body: Optional[str] = None

    created_at: datetime = Field(
        sa_column=Column(
            my.DATETIME,
            nullable=False,
            server_default=func.now()
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            my.DATETIME,
            nullable=False,
            server_default=func.now(),
            onupdate=func.now()
        )
    )

    def __repr__(self):
        return f"<Post {self.title}>"

    
