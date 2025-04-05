from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app import crud, schemas
from fastapi.responses import FileResponse , StreamingResponse
import aiohttp
import httpx
from aiohttp import ClientSession
from fastapi.responses import StreamingResponse

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/clips", response_model=list[schemas.ClipOut])
async def list_clips(db: AsyncSession = Depends(get_db)):
    return await crud.get_clips(db)

@router.post("/clips", response_model=schemas.ClipOut)
async def create_clip(clip: schemas.ClipCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_clip(db, clip)


@router.get("/clips/{clip_id}/stream")
async def stream_clip(clip_id: int, db: AsyncSession = Depends(get_db)):
    clip = await crud.get_clip(db, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")

    await crud.increment_play_count(db, clip)

    async def proxy_stream():
        async with ClientSession() as session:
            async with session.get(clip.audio_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=502, detail="Failed to fetch audio")
                async for chunk in response.content.iter_chunked(1024):
                    yield chunk

    return StreamingResponse(proxy_stream(), media_type="audio/mpeg")

@router.get("/clips/{clip_id}/stats", response_model=schemas.ClipOut)
async def get_stats(clip_id: int, db: AsyncSession = Depends(get_db)):
    clip = await crud.get_clip(db, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    return clip
