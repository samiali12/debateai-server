from database.session import session


class AiModeratorRepository:
    def __init__(self):
        self.db = session()

    def save_moderation_log(self, data: dict):
        pass
