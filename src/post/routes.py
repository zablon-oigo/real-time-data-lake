from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import PostCreate, PostUpdate, PostResponse
from src.db.main import get_session
from .services import PostService

post_service = PostService()
post_router = APIRouter(prefix="/posts", tags=["post"])


@post_router.get("", response_model=List[PostResponse])
async def get_all_posts(session: AsyncSession = Depends(get_session)):
    posts = await post_service.get_all_posts(session)
    return posts


@post_router.get("/{post_uid}", response_model=PostResponse)
async def get_post(post_uid: str, session: AsyncSession = Depends(get_session)):
    post = await post_service.get_post(post_uid, session)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@post_router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, session: AsyncSession = Depends(get_session)):
    new_post = await post_service.create_post(post_data, session)
    return new_post


@post_router.put("/{post_uid}", response_model=PostResponse)
async def update_post(post_uid: str, update_data: PostUpdate, session: AsyncSession = Depends(get_session)):
    updated_post = await post_service.update_post(post_uid, update_data, session)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return updated_post


@post_router.delete("/{post_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_uid: str, session: AsyncSession = Depends(get_session)):
    result = await post_service.delete_post(post_uid, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {}
