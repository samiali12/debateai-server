from modules.arguments.repository import ArgumentsRepository
from core.response import ApiResponse


class ArgumentService:
    def __init__(self):
        self.repo = ArgumentsRepository()

    def get_arguments(self, debate_id: int):
        arguments = self.repo.get_arguments(debate_id)
        formatted_data = [
            {
                "type": "argument",
                "debate_id": arg.debate_id,
                "user_id": arg.user_id,
                "fullName": arg.fullName,
                "role": arg.role,
                "content": arg.content,
                "timestamp": arg.timestamp.isoformat() if arg.timestamp else None,
                "toxicity_score": arg.toxicity_score,
                "civility_score": arg.civility_score,
                "flags": arg.flags,
            }
            for arg in arguments
        ]
        return ApiResponse(
            status_code=200, message="Arguments list", data=formatted_data
        )
