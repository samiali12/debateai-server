import json
from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect
from core.middleware import is_authenticated
from modules.auth.service import AuthService
from modules.debates.service import DebateService
from modules.debates.schemas import WSMessage
from modules.debates.schemas import DebateCreate, DebateUpdateStatus

router = APIRouter(prefix="/debates", tags=["debates"])

debate_service = DebateService()


def get_auth_service():
    return AuthService()


@router.post("/")
async def create_debate(
    request: DebateCreate,
    user: dict = Depends(is_authenticated),
    auth_service: AuthService = Depends(get_auth_service),
):
    userId = user.get("id")
    return debate_service.create_debate(request.title, request.description, userId)


@router.get("/")
async def list_debates(
    skip: int = 0,
    limit: int = 10,
    user: dict = Depends(is_authenticated),
    auth_service: AuthService = Depends(get_auth_service),
):
    return debate_service.list_debates(skip, limit)


@router.get("/{debate_id}")
async def get_debate(
    debate_id: int,
    user: dict = Depends(is_authenticated),
    auth_service: AuthService = Depends(get_auth_service),
):
    return debate_service.get_debate(debate_id)


@router.patch("/{debate_id}/status")
async def update_debate_status(
    debate_id: int,
    request: DebateUpdateStatus,
    user: dict = Depends(is_authenticated),
    auth_service: AuthService = Depends(get_auth_service),
):
    return debate_service.update_debate_status(debate_id, request.status)


@router.delete("/{debate_id}")
async def delete_debate(
    debate_id: int,
    user: dict = Depends(is_authenticated),
    auth_service: AuthService = Depends(get_auth_service),
):
    return debate_service.delete_debate(debate_id)


@router.websocket("/ws/debates/{room_id}")
async def debate_ws_endpoint(
    websocket: WebSocket,
    room_id: str,
    auth_service: AuthService = Depends(get_auth_service),
):
    await debate_service.connect(room_id, websocket)
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                json_data = json.loads(raw)
                message = WSMessage(**json_data)

            except json.JSONDecodeError as e:
                error = {
                    "type": "error",
                    "content": "invalid message format",
                    "detail": str(e),
                }
                await websocket.send_text(json.dumps(error))
                continue

            if message.type == "argument":
                logger_msg = (
                    f"[{message.role.upper()}] {message.user}: {message.content}"
                )
                print(logger_msg)
                await debate_service.broadcast(room_id, message.dict())
            elif message.type == "system":
                print(f"SYSTEM MESSAGE: {message.content}")
                await debate_service.broadcast(room_id, message.dict())
            else:
                print(f"Unknown message type: {message.type}")
                await websocket.send_text(
                    json.dumps({"type": "error", "content": "Unknown message type"})
                )

    except WebSocketDisconnect:
        debate_service.disconnect(room_id, websocket)
        leave_notice = {
            "type": "system",
            "content": f"A participant left room {room_id}",
        }
        await debate_service.broadcast(room_id, leave_notice)
