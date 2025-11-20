from pydantic import BaseModel
from typing import List, Optional

class ToneCivilityRequest(BaseModel):
    argument_id: int
    text: str

class ToneCivilityResponse(BaseModel):
    toxicity_score: float
    civility_score: float
    flags: str