from database.models.argument_civility_analysis import ArgumentCivilityAnalysis
from database.session import session
from core.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError


class ToneCivilityRepository:
    def __init__(self):
        self.db = session()

    def save_analysis(
        self,
        argument_id: int,
        toxicity_score: float,
        civility_score: float,
        flags: list,   # <— flags are list of strings
    ) -> ArgumentCivilityAnalysis:
        try:
            analysis = ArgumentCivilityAnalysis(
                argument_id=argument_id,
                toxicity_score=toxicity_score,
                civility_score=civility_score,
                flags=flags,
            )
            self.db.add(analysis)
            self.db.commit()
            self.db.refresh(analysis)
            return analysis

        except SQLAlchemyError as e:
            self.db.rollback()
            # 🔥 Add logging here if available
            raise HTTPException(
                status_code=500,
                detail=f"Database error while saving civility analysis."
            )

        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Unexpected error while saving civility analysis."
            )
