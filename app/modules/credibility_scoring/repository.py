from database.session import session
from database.models.argument_scores import ArgumentScores
from database.models.participants import Participants
from sqlalchemy.exc import SQLAlchemyError
from core.exceptions import DatabaseConnectionError
from core.logger import logger


class CredibilityScoreRepository:
    def __init__(self):
        self.db = session()

    def save_score(
        self,
        argument_id,
        participant_id,
        relevance,
        evidence,
        consistency,
        overall_strength,
        notes,
    ):
        try:
            participant = self.db.query(Participants).filter(Participants.user_id == participant_id).first()
            score = ArgumentScores(
                argument_id=argument_id,
                participant_id=participant.id,
                relevance_score=relevance,
                evidence_score=evidence,
                consistency_score=consistency,
                overall_strength=overall_strength,
                notes=notes,
            )
            self.db.add(score)
            self.db.commit()
            self.db.refresh(score)
            return score

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during debate creation: {str(e)}")
            raise DatabaseConnectionError()
