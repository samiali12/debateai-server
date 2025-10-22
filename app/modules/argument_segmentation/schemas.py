
from pydantic import BaseModel


class TextInput(BaseModel):
    text: str


class SegmentationResponse(BaseModel):
    segments: list[str]