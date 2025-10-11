from core.logger import logger
from core.exceptions import HTTPException
from database.session import session
from database.models.users import Users
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from core.exceptions import (
    UserAlreadyExistsError,
    DatabaseConnectionError,
    InvalidCredentialsError,
)
from core.security import verify_password, password_hashing


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

    def me(self, email: str):
        try:
            user = self.db.query(Users).filter(Users.email == email).first()
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during user creation: {str(e)}")
            raise DatabaseConnectionError()

    def change_password(self, email: str, old_password: str, new_password: str):
        try:
            user = self.db.query(Users).filter(Users.email == email).first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if not verify_password(user.password, old_password):
                raise HTTPException(status_code=400, detail="Old password is incorrect")

            hash = password_hashing(new_password)
            user.password = hash
            self.db.commit()
            self.db.refresh(user)
            logger.info(f"Password changed successfully for user {email}")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during user creation: {str(e)}")
            raise DatabaseConnectionError()

    def forget_password(self, email: str):
        try:
            user = self.db.query(Users).filter(Users.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during user forgetting password: {str(e)}")
            raise DatabaseConnectionError()

    def reset_password(self, email: str, new_password: str):
        try:
            user = self.db.query(Users).filter(Users.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            hash = password_hashing(new_password)
            user.password = hash
            self.db.commit()
            self.db.refresh(user)
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Database error during user resetting password: {str(e)}")
            raise DatabaseConnectionError()
