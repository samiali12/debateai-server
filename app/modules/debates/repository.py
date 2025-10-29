from database.session import session
from database.models.debates import Debates
from database.models.users import Users
from database.models.participants import Participants
from database.models.arguments import Arguments
from sqlalchemy.exc import SQLAlchemyError
from core.logger import logger
from core.exceptions import DatabaseConnectionError
from modules.debates.schemas import DebateResponse
from fastapi import HTTPException
from app.utils.constant import MAX_PARTICIPANTS, ROLE_LIMITS


class DebateRepository:
    def __init__(self):
        self.db = session()

    def create_debate(self, created_by: int, title: str, description: str, role: str):
        try:
            debate = Debates(
                title=title, description=description, created_by=created_by
            )
            self.db.add(debate)
            self.db.commit()
            self.db.refresh(debate)

            participant = Participants(
                debate_id=debate.id, user_id=created_by, role=role
            )

            self.db.add(participant)
            self.db.commit()

            formatted_data = debate.to_dict()

            return DebateResponse(**formatted_data)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during debate creation: {str(e)}")
            raise DatabaseConnectionError()

    def update_debate(self, debate_id: int, title: str, description: str, role: str):
        try:
            existing_dabate = (
                self.db.query(Debates).filter(Debates.id == debate_id).first()
            )
            if not existing_dabate:
                raise HTTPException(status_code=404, detail="Debate not found")

            if title != "":
                existing_dabate.title = title
            elif description != "":
                existing_dabate.description = description

            self.db.commit()
            self.db.refresh(existing_dabate)

            existing_participants = (
                self.db.query(Participants)
                .filter(
                    (Participants.user_id == existing_dabate.created_by)
                    and (Debates.id == existing_dabate.id)
                )
                .first()
            )

            if not existing_participants:
                raise HTTPException(
                    status_code=404, detail="participants not found in debate"
                )

            existing_participants.role = role

            self.db.commit()
            self.db.refresh(existing_participants)

            formatted_data = existing_dabate.to_dict()

            return DebateResponse(**formatted_data)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during debate creation: {str(e)}")
            raise DatabaseConnectionError()

    def join_debate(
        self,
        debate_id: int,
        partcipant_id: int,
        role: str,
    ):
        try:
            existing_dabate = (
                self.db.query(Debates).filter(Debates.id == debate_id).first()
            )
            if not existing_dabate:
                raise HTTPException(status_code=404, detail="Debate not found")

            existing_participant = (
                self.db.query(Participants)
                .filter(
                    (Participants.user_id == partcipant_id)
                    & (Participants.debate_id == existing_dabate.id)
                )
                .first()
            )

            if existing_participant:
                raise HTTPException(
                    status_code=409, detail="Participant is already exists"
                )

            participants_list = (
                self.db.query(Participants)
                .filter(Participants.debate_id == existing_dabate.id)
                .all()
            )

            if len(participants_list) == MAX_PARTICIPANTS:
                raise HTTPException(status_code=400, detail="Debate is already full")

            role_count = (
                self.db.query(Participants)
                .filter(Participants.debate_id == debate_id, Participants.role == role)
                .count()
            )

            print("Total role ==> ", role_count)
            print("ss ==> ", ROLE_LIMITS.get(role, 0))

            if role_count >= ROLE_LIMITS.get(role, 0):
                raise HTTPException(
                    status_code=400, detail=f"No more spots for role '{role}'"
                )

            new_participant = Participants(
                debate_id=existing_dabate.id, user_id=partcipant_id, role=role
            )
            self.db.add(new_participant)
            self.db.commit()

            formatted_data = existing_dabate.to_dict()

            return DebateResponse(**formatted_data)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during participant join debate: {str(e)}")
            raise DatabaseConnectionError()

    def get_debate_by_id(self, debate_id: int):
        try:
            debate = self.db.query(Debates).filter(Debates.id == debate_id).first()
            if debate:
                formatted_data = debate.__dict__.copy()
                formatted_data["status"] = formatted_data["status"].value
                return DebateResponse(**formatted_data)
            return None
        except SQLAlchemyError as e:
            logger.error(f"Database error during fetching debate by ID: {str(e)}")
            raise DatabaseConnectionError()

    def list_debates(self, skip: int = 0, limit: int = 10):
        try:
            debates = self.db.query(Debates).offset(skip).limit(limit).all()
            response = []
            for debate in debates:
                formatted_data = debate.__dict__.copy()
                formatted_data["status"] = formatted_data["status"].value
                response.append(DebateResponse(**formatted_data))
            return response
        except SQLAlchemyError as e:
            logger.error(f"Database error during listing debates: {str(e)}")
            raise DatabaseConnectionError()

    def get_participants_lists(self, debate_id):
        participants = (
            self.db.query(
                Participants.id,
                Users.id.label("user_id"),
                Users.fullName,
                Users.email,
                Participants.role,
            )
            .join(Users, Users.id == Participants.user_id)
            .filter(Participants.debate_id == debate_id)
            .all()
        )
        print("part ==> ", participants)
        format_participants = [
            {
                "participantId": p[0],
                "userId": p[1],
                "fullName": p[2],
                "email": p[3],
                "role": p[4].name,
            }
            for p in participants
        ]
        return format_participants

    def update_debate_status(self, debate_id: int, new_status: str):
        try:
            debate = self.db.query(Debates).filter(Debates.id == debate_id).first()
            if not debate:
                return None
            debate.status = new_status
            self.db.commit()
            self.db.refresh(debate)

            formatted_data = debate.__dict__.copy()
            formatted_data["status"] = formatted_data["status"].value

            return DebateResponse(**formatted_data)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during updating debate status: {str(e)}")
            raise DatabaseConnectionError()

    def delete_debate(self, debate_id: int):
        try:
            debate = self.db.query(Debates).filter(Debates.id == debate_id).first()
            if not debate:
                return False
            self.db.delete(debate)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during deleting debate: {str(e)}")
            raise DatabaseConnectionError()

    def save_argument(self, debate_id: int, user_id: int, role: str, content: str):
        try:
            debate = self.db.query(Debates).filter(Debates.id == debate_id).first()
            if not debate:
                raise HTTPException(status_code=404, detail="Debate not found")
            argument = Arguments(
                debate_id=debate_id, user_id=user_id, role=role, content=content
            )
            self.db.add(argument)
            self.db.commit()
            self.db.refresh(argument)
            return argument

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during saving argument: {str(e)}")
            raise DatabaseConnectionError()
