import json

from django.http import HttpRequest, JsonResponse
from poker.services.items_service import ItemService

class ItemController:
    def __init__(self):
        self.service = ItemService()

    def create(self, request: HttpRequest):
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None, JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        self.service.create(
            title=payload.get("title"),
            description=payload.get("description"),
            session_id=payload.get("session_id"),
            position=payload.get("position"),
            status=payload.get("status"),
            created_by_roblox_user_id=payload.get("created_by_roblox_user_id"),
        )

    def get_by_id(self, request: HttpRequest, item_id: int):
        return self.service.get_by_id(item_id)
    
    def get_by_session_id(self, request: HttpRequest, session_id: int):
        return self.service.get_by_session_id(session_id)
    
    def get_by_session_and_position(
            self, request: HttpRequest, 
            session_id: int, 
            position: int
    ):
        return self.service.get_by_session_and_position(session_id, position)
    
    def update(self, request: HttpRequest, item_id: int):
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None, JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        self.service.update(
            item_id=item_id,
            title=payload.get("title"),
            description=payload.get("description"),
            position=payload.get("position"),
            status=payload.get("status"),
        )
    
    def delete(self, request: HttpRequest, item_id: int):
        return self.service.delete(item_id)
