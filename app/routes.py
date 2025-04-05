from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app import crud, schemas
from fastapi.responses import FileResponse
import aiohttp

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/clips", response_model=list[schemas.ClipOut])
async def list_clips(db: AsyncSession = Depends(get_db)):
    return await crud.get_clips(db)

@router.get("/clips/{clip_id}/stream")
async def stream_clip(clip_id: int, db: AsyncSession = Depends(get_db)):
    clip = await crud.get_clip(db, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    await crud.increment_play_count(db, clip)
    return FileResponse(path=clip.audio_url, media_type='audio/mpeg')

@router.get("/clips/{clip_id}/stats", response_model=schemas.ClipOut)
async def get_stats(clip_id: int, db: AsyncSession = Depends(get_db)):
    clip = await crud.get_clip(db, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    return clip
