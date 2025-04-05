from pydantic import BaseModel

class ClipBase(BaseModel):
    title: str
    description: str
    genre: str
    duration: str
    audio_url: str

class ClipCreate(ClipBase):
    pass

class ClipOut(ClipBase):
    id: int
    play_count: int

    class Config:
        orm_mode = True
