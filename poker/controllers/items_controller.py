import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from poker.serializers import ItemSerializer
from poker.services.items_service import ItemService

class ItemController:
    def __init__(self):
        self.service = ItemService()

    def create(self, request: HttpRequest) -> HttpResponse:
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        # Validation des champs requis
        required_fields = ["title", "description", "session_id", "status", "created_by_roblox_user_id"]
        missing = [field for field in required_fields if payload.get(field) in [None, ""]]
        if missing:
            return JsonResponse({"error": f"Missing or empty fields: {', '.join(missing)}"}, status=400)

        # Validation des types
        if not isinstance(payload["title"], str) or not payload["title"].strip():
            return JsonResponse({"error": "Title must be a non-empty string."}, status=400)
        if not isinstance(payload["description"], str):
            return JsonResponse({"error": "Description must be a string."}, status=400)
        if not isinstance(payload["session_id"], int):
            return JsonResponse({"error": "Session ID must be an integer."}, status=400)
        if not isinstance(payload["status"], str):
            return JsonResponse({"error": "Status must be a string."}, status=400)
        if not isinstance(payload["created_by_roblox_user_id"], int):
            return JsonResponse({"error": "created_by_roblox_user_id must be an integer."}, status=400)
        
        item = self.service.create(
            title=payload.get("title"),
            description=payload.get("description"),
            session_id=payload.get("session_id"),
            status=payload.get("status"),
            created_by_roblox_user_id=payload.get("created_by_roblox_user_id"),
        )

        serialized_item = ItemSerializer(item)
        return JsonResponse(serialized_item.data, status=201, safe=False)

    def get_by_id(self, request: HttpRequest, item_id: int) -> HttpResponse:
        item = self.service.get_by_id(item_id)
        if not item:
            return JsonResponse({"error": "Item not found."}, status=404)
        
        serialized_item = ItemSerializer(item)
        return JsonResponse(serialized_item.data, status=200, safe=False)
    
    def get_by_session_id(self, request: HttpRequest, session_id: int) -> HttpResponse:
        items = self.service.get_by_session_id(session_id)
        if not items:
            return JsonResponse({"error": "Items not found."}, status=404)
        
        serialized_item = [ItemSerializer(item).data for item in items]
        return JsonResponse(serialized_item, status=200, safe=False)
    
    def get_by_session_and_position(
            self, 
            request: HttpRequest, 
            session_id: int, 
            position: int
    ) -> HttpResponse:
        item = self.service.get_by_session_and_position(session_id, position)
        if not item:
            return JsonResponse({"error": "Item not found"}, status=404)
        
        serialized_item = ItemSerializer(item)
        return JsonResponse(serialized_item.data, status=200, safe=False)

    
    def update(self, request: HttpRequest, item_id: int) -> HttpResponse:
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        if "title" in payload and (not isinstance(payload["title"], str) or not payload["title"].strip()):
            return JsonResponse({"error": "Title must be a non-empty string."}, status=400)
        if "description" in payload and not isinstance(payload["description"], str):
            return JsonResponse({"error": "Description must be a string."}, status=400)
        if "position" in payload and not isinstance(payload["position"], int):
            return JsonResponse({"error": "Position must be an integer."}, status=400)
        if "status" in payload and not isinstance(payload["status"], str):
            return JsonResponse({"error": "Status must be a string."}, status=400)

        item = self.service.update(
            item_id=item_id,
            title=payload.get("title"),
            description=payload.get("description"),
            position=payload.get("position"),
            status=payload.get("status"),
        )

        serialized_item = ItemSerializer(item)
        return JsonResponse(serialized_item.data, status=200, safe=False)
    
    def delete(self, request: HttpRequest, item_id: int) -> HttpResponse:
        item = self.service.delete(item_id)
        serialized_item = ItemSerializer(item)
        return JsonResponse(serialized_item.data, status=201, safe=False)
