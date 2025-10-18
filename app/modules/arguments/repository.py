from database.session import session
from fastapi import HTTPException
from modules.arguments.schemas import ArgumentResponse
from database.models.debates import Debates
from database.models.arguments import Arguments
from database.models.users import Users
from database.models.participants import Participants
from sqlalchemy.orm import joinedload


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
            )
            .join(Users, Users.id == Arguments.user_id)
            .filter(Arguments.debate_id == debate.id)
            .all()
        )

        formatted_data = [
            {
                "type": "argument",
                "debate_id": arg.debate_id,
                "user_id": arg.user_id,
                "fullName": arg.fullName,
                "role": arg.role,
                "content": arg.content,
                "timestamp": arg.timestamp.isoformat() if arg.timestamp else None,
            }
            for arg in arguments
        ]
        return formatted_data
