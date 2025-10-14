from database.session import session
from database.models.debates import Debates
from sqlalchemy.exc import SQLAlchemyError
from core.logger import logger
from core.exceptions import DatabaseConnectionError
from modules.debates.schemas import DebateResponse


class DebateRepository:
    def __init__(self):
        self.db = session()

    def create_debate(self, title: str, description: str, created_by: int):
        try:
            debate = Debates(
                title=title, description=description, created_by=created_by
            )
            self.db.add(debate)
            self.db.commit()
            self.db.refresh(debate)

            formatted_data = debate.__dict__.copy()
            formatted_data["status"] = formatted_data["status"].value

            return DebateResponse(**formatted_data)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during debate creation: {str(e)}")
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
