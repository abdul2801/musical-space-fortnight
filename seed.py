import asyncio
from app.models import Clip
from app.database import engine, AsyncSessionLocal
from app.database import Base

dummy_clips = [
    {
        "title": "Ocean Waves",
        "description": "Soothing ocean sounds",
        "genre": "ambient",
        "duration": "30s",
        "audio_url": "https://github.com/abdul2801/musical-space-fortnight/raw/codespace-musical-space-fortnight-p6r64vrjvjphr557/static/audio/ocean.mp3"
    },
    {
        "title": "Chill Lo-Fi",
        "description": "Relaxing lo-fi beat",
        "genre": "lo-fi",
        "duration": "30s",
        "audio_url": "https://github.com/abdul2801/musical-space-fortnight/raw/codespace-musical-space-fortnight-p6r64vrjvjphr557/static/audio/chill.mp3"
    },
    {
        "title": "Classical Vibes",
        "description": "Peaceful classical piano",
        "genre": "classical",
        "duration": "30s",
        "audio_url": "https://github.com/abdul2801/musical-space-fortnight/raw/codespace-musical-space-fortnight-p6r64vrjvjphr557/static/audio/classical.mp3"
    },
    {
        "title": "Helix",
        "description": "Peaceful classical piano",
        "genre": "classical",
        "duration": "30s",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    },
]
async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        for clip in dummy_clips:
            session.add(Clip(**clip))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
