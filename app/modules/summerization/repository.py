from database.session import session
from database.models.summaries import Summaries
from sqlalchemy.exc import SQLAlchemyError
from core.exceptions import DatabaseConnectionError


class SummerizationRepository:

    def __init__(self):
        self.db = session()

    def create_summary(self, debate_id: int, url: str):
        try:
            record = (
                self.db.query(Summaries)
                .filter(Summaries.debate_id == debate_id)
                .first()
            )

            if record:
                record.download_url = url
                self.db.commit()
                self.db.refresh(record)
                return record.download_url

            new_record = Summaries(
                debate_id=debate_id,
                download_url=url
            )
            self.db.add(new_record)
            self.db.commit()
            self.db.refresh(new_record)
            return new_record.download_url

        except SQLAlchemyError:
            self.db.rollback()
            raise DatabaseConnectionError()

    def get_summary(self, debate_id: int):
        try:
            record = (
                self.db.query(Summaries)
                .filter(Summaries.debate_id == debate_id)
                .first()
            )
            return record.download_url if record else None

        except SQLAlchemyError:
            self.db.rollback()
            raise DatabaseConnectionError()
