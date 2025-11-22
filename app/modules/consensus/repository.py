from database.session import session
from typing import List, Dict, Any, Optional
from database.models.arguments import Arguments
from database.models.consensus_recommendations import ConsensusRecommendation


class ConsensusRepository:
    def __init__(self):
        self.db = session()

    def get_messages_by_debate_and_role(
        self, debate_id: int, role: str
    ) -> List[Dict[str, Any]]:
        q = self.db.query(Arguments).filter(Arguments.debate_id == debate_id)
        q = q.filter(Arguments.role.ilike(role))
        rows = q.order_by(Arguments.created_at.asc()).all()
        return [
            {
                "id": r.id,
                "content": r.content,
                "created_at": r.created_at,
                "author_id": getattr(r, "author_id", None),
            }
            for r in rows
        ]

    def get_all_messages_by_debate(self, debate_id: int) -> List[Dict[str, Any]]:
        rows = (
            self.db.query(Arguments)
            .filter(Arguments.debate_id == debate_id)
            .order_by(Arguments.created_at.asc())
            .all()
        )
        return [
            {
                "id": r.id,
                "content": r.content,
                "role": r.role,
                "created_at": r.created_at,
            }
            for r in rows
        ]

    def save_recommendation(
        self,
        debate_id: int,
        payload: Dict[str, Any],
        summary_text: str,
        generated_by: str = "system",
    ) -> ConsensusRecommendation:
        rec = ConsensusRecommendation(
            debate_id=debate_id,
            payload=payload,
            summary_text=summary_text,
            generated_by=generated_by,
        )
        self.db.add(rec)
        self.db.commit()
        self.db.refresh(rec)
        return rec

    def get_latest_recommendation(
        self, debate_id: int
    ) -> Optional[ConsensusRecommendation]:
        return (
            self.db.query(ConsensusRecommendation)
            .filter(ConsensusRecommendation.debate_id == debate_id)
            .order_by(ConsensusRecommendation.generated_at.desc())
            .first()
        )
