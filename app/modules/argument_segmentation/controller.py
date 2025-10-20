from fastapi import APIRouter, Depends, HTTPException
from core.response import ApiResponse
from modules.argument_segmentation.schemas import TextInput, SegmentationResponse
from modules.argument_segmentation.service import ArgumentSegmentationService

service = ArgumentSegmentationService()

router = APIRouter(prefix="/argument-segmentation", tags=["Argument Segmentation"])


@router.post("/segment", response_model=ApiResponse)
async def segment_text(payload: TextInput):
    try:
        segments = service.segment_arguments(payload.text)

        return ApiResponse(
            data=SegmentationResponse(segments=segments).dict(),
            message="Text segmented successfully.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
