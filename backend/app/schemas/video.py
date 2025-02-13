from pydantic import BaseModel
from typing import List

class FrameExtractResponse(BaseModel):
    session_id: str
    frame_count: int
    frames: List[str] 