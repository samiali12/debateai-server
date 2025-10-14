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
