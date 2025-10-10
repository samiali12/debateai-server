from core.logger import logger
from database.session import session
from database.models.users import Users
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.exceptions import (
    UserAlreadyExistsError,
    DatabaseConnectionError,
    InvalidCredentialsError,
)
from core.security import verify_password


class AuthRepository:
    def __init__(self):
        self.db = session()

    def create_user(self, fullName, email, password, role):
        try:
            user = Users(fullName=fullName, email=email, password=password, role=role)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user

        except IntegrityError:
            self.db.rollback()
            logger.warning(f"Duplicate email detected: {email}")
            raise UserAlreadyExistsError(email)

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during user creation: {str(e)}")
            raise DatabaseConnectionError()

    def login_user(self, email, password):
        try:
            user = self.db.query(Users).filter(Users.email == email).first()
            if not user:
                raise InvalidCredentialsError(message="Invalid email")
            flag = verify_password(user.password, password)
            if flag:
                return user
            else:
                raise InvalidCredentialsError(message="Invalid Password")

        except Exception as e:
            raise InvalidCredentialsError()

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during user creation: {str(e)}")
            raise DatabaseConnectionError()
