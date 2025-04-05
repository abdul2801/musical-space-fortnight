from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app import crud, schemas
from fastapi.responses import FileResponse , StreamingResponse , PlainTextResponse
import aiohttp
import httpx
from aiohttp import ClientSession
from fastapi.responses import StreamingResponse
from prometheus_client import Counter

router = APIRouter()
stream_counter = Counter(
    "stream_requests_total", 
    "Total stream requests",
    ["clip_id"]
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/", response_class=PlainTextResponse)
def root():
    return """API Endpoints
Method    Endpoint                       Description
GET       /clips                        List all available audio clips
POST      /clips                        Create a new audio clip entry
GET       /clips/{clip_id}/stream       Stream the audio clip
GET       /clips/{clip_id}/stats        Get play count and clip metadata
GET       /metrics                      Prometheus metrics export
"""


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
    stream_counter.labels(clip_id=str(clip_id)).inc()



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
