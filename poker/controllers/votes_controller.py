import json

from django.http import HttpRequest, JsonResponse

from poker.services.votes_service import VotesService

class VotesController:
    def __init__(self):
        self.service = VotesService()

    def create(self, request: HttpRequest):
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None, JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        # Validation des champs requis
        required_fields = ["item_id", "roblox_user_id", "value"]
        missing = [field for field in required_fields if payload.get(field) in [None, ""]]
        if missing:
            return None, JsonResponse({"error": f"Missing or empty fields: {', '.join(missing)}"}, status=400)
        
        # Validation des types
        if not isinstance(payload["item_id"], int):
            return None, JsonResponse({"error": "item_id must be an integer."}, status=400)
        if not isinstance(payload["value"], int):
            return None, JsonResponse({"error": "value must be an integer."}, status=400)
        if not isinstance(payload["roblox_user_id"], int):
            return None, JsonResponse({"error": "roblox_user_id must be an integer."}, status=400)
        
        self.service.create(
            item_id=payload.get("item_id"),
            value=payload.get("value"),
            roblox_user_id=payload.get("roblox_user_id"),
        )

    def update(self, request: HttpRequest, vote_id: int):
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None, JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        if not isinstance(payload["value"], int):
            return None, JsonResponse({"error": "value must be an integer."}, status=400)
        
        self.service.update(vote_id=vote_id, value=payload.get('value'))

    def delete(self, request: HttpRequest, vote_id: int):
        return self.service.delete(vote_id=vote_id)