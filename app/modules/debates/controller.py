import json
from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect
from core.middleware import is_authenticated
from modules.debates.service import DebateService
from modules.debates.schemas import WSMessage
from modules.debates.schemas import (
    DebateCreate,
    DebateUpdateStatus,
    DebateUpdate,
    JoinDebateRequest,
)

router = APIRouter(prefix="/debates", tags=["debates"])

debate_service = DebateService()


@router.post("/")
async def create_debate(
    request: DebateCreate,
    user: dict = Depends(is_authenticated),
):
    userId = user.get("id")
    return debate_service.create_debate(
        userId, request.title, request.description, request.role
    )


@router.patch("/{id}")
async def update_debate(
    request: DebateUpdate,
    user: dict = Depends(is_authenticated),
):
    return debate_service.update_debate(
        id, request.title, request.description, request.role
    )


@router.patch("/{id}/join")
async def joined_debate(
    id: int,
    request: JoinDebateRequest,
    user: dict = Depends(is_authenticated),
):
    user_id = user["id"]
    return debate_service.join_debate(
        debate_id=id, partcipant_id=user_id, role=request.role
    )


@router.get("/{debate_id}/participants")
async def get_participants(debate_id: int):
    return debate_service.get_participants_list(debate_id)


@router.get("/")
async def list_debates(
    skip: int = 0,
    limit: int = 10,
    user: dict = Depends(is_authenticated),
):
    return debate_service.list_debates(skip, limit)


@router.get("/{debate_id}")
async def get_debate(
    debate_id: int,
    user: dict = Depends(is_authenticated),
):
    return debate_service.get_debate(debate_id)


@router.patch("/{debate_id}/status")
async def update_debate_status(
    debate_id: int,
    request: DebateUpdateStatus,
    user: dict = Depends(is_authenticated),
):
    return debate_service.update_debate_status(debate_id, request.status)


@router.delete("/{debate_id}")
async def delete_debate(
    debate_id: int,
    user: dict = Depends(is_authenticated),
):
    return debate_service.delete_debate(debate_id)


@router.websocket("/ws/debates/{debate_id}")
async def debate_ws_endpoint(
    websocket: WebSocket,
    debate_id: str,
    # user: dict = Depends(is_authenticated),
):
    await debate_service.connect(debate_id, websocket)
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
                debate_service.save_argument(
                    message.debate_id, message.user_id, message.role, message.content
                )
                await debate_service.broadcast(debate_id, message.dict())

            else:
                print(f"Unknown message type: {message.type}")
                await websocket.send_text(
                    json.dumps({"type": "error", "content": "Unknown message type"})
                )

    except WebSocketDisconnect:
        debate_service.disconnect(debate_id, websocket)
        leave_notice = {
            "type": "system",
            "content": f"A participant left room {debate_id}",
        }
        await debate_service.broadcast(debate_id, leave_notice)
