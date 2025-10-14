import json
from fastapi import WebSocket, HTTPException
from typing import Dict, Set
from core.logger import logger
from modules.debates.repository import DebateRepository
from core.response import ApiResponse


class DebateService:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.repo = DebateRepository()

    def create_debate(self, title: str, description: str, created_by: int):
        debate = self.repo.create_debate(title, description, created_by)
        return ApiResponse(
            success=201, message="Debate created successfully", data=debate
        )

    def get_debate(self, debate_id: int):
        debate = self.repo.get_debate_by_id(debate_id)
        if debate:
            return ApiResponse(
                success=True, message="Debate fetched successfully", data=debate
            )
        raise HTTPException(status_code=404, detail="Debate not found")

    def list_debates(self, skip: int = 0, limit: int = 10):
        debates = self.repo.list_debates(skip, limit)
        return ApiResponse(
            success=200, message="Debates fetched successfully", data=debates
        )

    def update_debate_status(self, debate_id: int, new_status: str):
        debate = self.repo.update_debate_status(debate_id, new_status)
        if debate:
            return ApiResponse(
                success=True, message="Debate status updated successfully", data=debate
            )
        raise HTTPException(status_code=404, detail="Debate not found")

    def delete_debate(self, debate_id: int):
        success = self.repo.delete_debate(debate_id)
        if success:
            return ApiResponse(
                success=True, message="Debate deleted successfully", data=None
            )
        raise HTTPException(status_code=404, detail="Debate not found")

    async def _connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        room = self.active_connections.setdefault(room_id, set())
        room.add(websocket)
        logger.debug("WS connect %s -> room %s", id(websocket), room_id)

    async def _disconnect(self, room_id: str, websocket: WebSocket):
        room = self.active_connections.get(room_id)
        if not room:
            return
        if websocket in room:
            room.remove(websocket)
            logger.debug("WS disconnect %s -> room %s", id(websocket), room_id)
            if not room:
                del self.active_connections[room_id]
                logger.debug("Room %s empty, deleted", room_id)

    def connect(self, room_id: str, websocket: WebSocket):
        return self._connect(room_id, websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        return self._disconnect(room_id, websocket)

    async def broadcast(self, room_id: str, message: dict):
        conns = self.active_connections.get(room_id)
        if not conns:
            return
        payload = json.dumps(message)
        for ws in list(conns):
            try:
                await ws.send_text(payload)
            except Exception as e:
                logger.warning("Broadcast send failed, disconnecting: %s", e)
                try:
                    self._disconnect(room_id, ws)
                except Exception:
                    pass

    def save_argument(self, debate_id: int, user_id: int, role: str, content: str):
        argument = self.repo.save_argument(debate_id, user_id, role, content)
        if argument:
            return ApiResponse(
                success=True, message="Argument saved successfully", data=argument
            )
