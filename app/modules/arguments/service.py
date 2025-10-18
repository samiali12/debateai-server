from modules.arguments.repository import ArgumentsRepository
from core.response import ApiResponse


class ArgumentService:
    def __init__(self):
        self.repo = ArgumentsRepository()

    def get_arguments(self, debate_id: int):
        data = self.repo.get_arguments(debate_id)
        return ApiResponse(status_code=200, message="Arguments list", data=data)
