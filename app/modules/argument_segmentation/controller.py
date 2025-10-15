from fastapi import APIRouter, Depends
from modules.argument_segmentation.schemas import TextInput, SegmentationResponse
from core.middleware import is_authenticated
from utils.text_processing import process_text

router = APIRouter(prefix="/argument-segmentation", tags=["Argument Segmentation"])


@router.post("/process")
async def segment_text_endpoint(payload: TextInput, user=Depends(is_authenticated)):
    result = process_text(payload.text)
    return result
