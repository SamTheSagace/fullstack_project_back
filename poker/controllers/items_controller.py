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
        
        # Validation des champs requis
        required_fields = ["title", "description", "session_id", "position", "status", "created_by_roblox_user_id"]
        missing = [field for field in required_fields if payload.get(field) in [None, ""]]
        if missing:
            return None, JsonResponse({"error": f"Missing or empty fields: {', '.join(missing)}"}, status=400)

        # Validation des types
        if not isinstance(payload["title"], str) or not payload["title"].strip():
            return None, JsonResponse({"error": "Title must be a non-empty string."}, status=400)
        if not isinstance(payload["description"], str):
            return None, JsonResponse({"error": "Description must be a string."}, status=400)
        if not isinstance(payload["session_id"], int):
            return None, JsonResponse({"error": "Session ID must be an integer."}, status=400)
        if not isinstance(payload["position"], int):
            return None, JsonResponse({"error": "Position must be an integer."}, status=400)
        if not isinstance(payload["status"], str):
            return None, JsonResponse({"error": "Status must be a string."}, status=400)
        if not isinstance(payload["created_by_roblox_user_id"], int):
            return None, JsonResponse({"error": "created_by_roblox_user_id must be an integer."}, status=400)
        
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
        
        if "title" in payload and (not isinstance(payload["title"], str) or not payload["title"].strip()):
            return None, JsonResponse({"error": "Title must be a non-empty string."}, status=400)
        if "description" in payload and not isinstance(payload["description"], str):
            return None, JsonResponse({"error": "Description must be a string."}, status=400)
        if "position" in payload and not isinstance(payload["position"], int):
            return None, JsonResponse({"error": "Position must be an integer."}, status=400)
        if "status" in payload and not isinstance(payload["status"], str):
            return None, JsonResponse({"error": "Status must be a string."}, status=400)

        self.service.update(
            item_id=item_id,
            title=payload.get("title"),
            description=payload.get("description"),
            position=payload.get("position"),
            status=payload.get("status"),
        )
    
    def delete(self, request: HttpRequest, item_id: int):
        return self.service.delete(item_id)
