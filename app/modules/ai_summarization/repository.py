from typing import List
from database.session import session
from app.modules.arguments.repository import ArgumentsRepository

class ArgumentSumerizationRepository:
    def __init__(self):
        self.argument_repo = ArgumentsRepository()

    def get_segmented_arguments(self, debate_id: int):
        self.argument_repo.get_arguments(debate_id)