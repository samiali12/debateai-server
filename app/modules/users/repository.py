from database.session import session
from database.models.users import Users


class UserRepository:
    def __init__(self):
        self.db = session()

    def get_user_by_email(self, email: str):
        return self.db.query(Users).filter(Users.email == email).first()

    def update_user(self, user: Users, update_data: dict):
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
