import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from poker.serializers import VoteSerializer
from poker.services.votes_service import VotesService

class VotesController:
    def __init__(self):
        self.service = VotesService()

    def create(self, request: HttpRequest) -> HttpResponse:
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        # Validation des champs requis
        required_fields = ["item_id", "roblox_user_id", "value"]
        missing = [field for field in required_fields if payload.get(field) in [None, ""]]
        if missing:
            return JsonResponse({"error": f"Missing or empty fields: {', '.join(missing)}"}, status=400)
        
        # Validation des types
        if not isinstance(payload["item_id"], int):
            return JsonResponse({"error": "item_id must be an integer."}, status=400)
        if not isinstance(payload["value"], int):
            return JsonResponse({"error": "value must be an integer."}, status=400)
        if not isinstance(payload["roblox_user_id"], int):
            return JsonResponse({"error": "roblox_user_id must be an integer."}, status=400)
        
        vote = self.service.create(
            item_id=payload.get("item_id"),
            value=payload.get("value"),
            roblox_user_id=payload.get("roblox_user_id"),
        )
        serialized_vote = VoteSerializer(vote)
        return JsonResponse(serialized_vote.data, status=201, safe=False)

    def update(self, request: HttpRequest, vote_id: int) -> HttpResponse:
        try:
            body = request.body.decode("utf-8") if request.body else "{}"
            payload = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return JsonResponse({"error": "Invalid JSON body."}, status=400)
        
        if not isinstance(payload["value"], int):
            return JsonResponse({"error": "value must be an integer."}, status=400)
        
        vote = self.service.update(vote_id=vote_id, value=payload.get('value'))
        serialized_vote = VoteSerializer(vote)
        return JsonResponse(serialized_vote.data, status=200, safe=False)

    def delete(self, request: HttpRequest, vote_id: int) -> HttpResponse:
        vote = self.service.delete(vote_id=vote_id)
        serialized_vote = VoteSerializer(vote)
        return JsonResponse(serialized_vote.data, status=200, safe=False)