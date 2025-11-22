from fastapi import APIRouter, HTTPException
from .schemas import ConsensusResponse
from .service import ConsensusService
from typing import Any, Dict

router = APIRouter(prefix="/consensus", tags=["Consensus"])


@router.get("/{debate_id}/generate", response_model=ConsensusResponse)
def generate_consensus(debate_id: int):
    try:
        svc = ConsensusService()
        result = svc.generate_consensus(debate_id, save=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{debate_id}", response_model=Dict[str, Any])
def get_latest_consensus(debate_id: int):
    try:
        svc = ConsensusService()
        payload = svc.get_latest_consensus(debate_id)
        if not payload:
            raise HTTPException(
                status_code=404, detail="No consensus found for this debate"
            )
        return payload
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
