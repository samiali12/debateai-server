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
            }
            for arg in arguments
        ]
        text = self.segmentation_service.segment_arguments(
            text="Electric cars are eco-friendly. However, gas cars are more affordable."
        )
        print(text)
        return ApiResponse(
            status_code=200, message="Arguments list", data=formatted_data
        )
