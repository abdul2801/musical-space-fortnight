from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.models import Clip

async def get_clips(db: AsyncSession):
    result = await db.execute(select(Clip))
    return result.scalars().all()

async def get_clip(db: AsyncSession, clip_id: int):
    return await db.get(Clip, clip_id)

async def increment_play_count(db: AsyncSession, clip: Clip):
    clip.play_count += 1
    db.add(clip)
    await db.commit()
