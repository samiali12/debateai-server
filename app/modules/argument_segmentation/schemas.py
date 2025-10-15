from pydantic import BaseModel 

class TextInput(BaseModel):
    text: str  

class SegmentationResponse(BaseModel):
    original_text: str
    segments: list[str]