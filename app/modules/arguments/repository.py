from database.session import session
from fastapi import HTTPException
from database.models.debates import Debates
from database.models.arguments import Arguments
from database.models.users import Users
from database.models.argument_civility_analysis import ArgumentCivilityAnalysis


class ArgumentsRepository:
    def __init__(self):
        self.db = session()

    def get_arguments(self, debate_id: int):
        debate = self.db.query(Debates).filter(Debates.id == debate_id).first()
        if not debate:
            HTTPException(status_code=404, detail="Debate not found")
        arguments = (
            self.db.query(
                Arguments.id,
                Arguments.debate_id,
                Arguments.user_id,
                Users.fullName,
                Arguments.role,
                Arguments.content,
                Arguments.created_at.label("timestamp"),
                ArgumentCivilityAnalysis.toxicity_score,
                ArgumentCivilityAnalysis.civility_score,
                ArgumentCivilityAnalysis.flags,
            )
            .join(Users, Users.id == Arguments.user_id)
            .outerjoin(
                ArgumentCivilityAnalysis,
                ArgumentCivilityAnalysis.argument_id == Arguments.id,
            )
            .filter(Arguments.debate_id == debate.id)
            .order_by(Arguments.created_at.asc())
            .all()
        )
        print("ist ==> ", arguments)
        return arguments
