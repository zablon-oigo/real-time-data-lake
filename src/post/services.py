from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.models import Post 
from .schemas import PostCreate, PostUpdate
from sqlmodel import select, desc
from src.config import Config
from src.producer import kafka_producer
from datetime import datetime, timezone



class PostService:
    async def get_all_posts(self, session: AsyncSession):
        stmt = select(Post).order_by(desc(Post.created_at))
        res = await session.exec(stmt)
        return res.all()
    
    async def get_post(self, post_uid: str, session: AsyncSession):
        stmt = select(Post).where(Post.uid == post_uid)
        res = await session.exec(stmt)
        return res.first()

    async def create_post(self, post_data: PostCreate, session):
        new_post = Post(**post_data.model_dump())
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)

        kafka_producer.publish(
            topic=Config.KAFKA_TOPIC_POSTS,
            data={
                "event_type": "created",
                "uuid": str(new_post.uid),
                "title": new_post.title,
                "body": new_post.body,
                "timestamp": datetime.now(timezone.utc).isoformat()  
            }
        )
        return new_post

    async def update_post(self, post_uid, update_data: PostUpdate, session):
        post = await self.get_post(post_uid, session)
        if not post:
            return None

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)

        await session.commit()
        await session.refresh(post)

        kafka_producer.publish(
            topic=Config.KAFKA_TOPIC_POSTS,
            data={
                "event_type": "updated",
                "uuid": str(post.uid),
                "title": post.title,
                "body": post.body,
                "timestamp": datetime.now(timezone.utc).isoformat() 
            }
        )

        return post
    
    async def delete_post(self, post_uid: str, session: AsyncSession):
        post = await self.get_post(post_uid, session)
        
        if not post:
            return None
        
        await session.delete(post)
        await session.commit()
        
        return {"deleted": True}
