from django.http import HttpRequest, HttpResponse, JsonResponse

from poker.helpers.utils import parse_json_body
from poker.serializers import SessionSerializer
from poker.services.sessions_service import SessionService


class SessionController:
    def __init__(self):
        self.service = SessionService()

    def list(self, request: HttpRequest, serv_id: str) -> HttpResponse:
        try:
            sessions_payload = self.service.list_waiting_with_members(serv_id)
            serialized_payload = [SessionSerializer(session).data for session in sessions_payload]
            return JsonResponse({"sessions": serialized_payload}, status=200)
        except Exception:
            return JsonResponse({"error": "Failed to retrieve waiting sessions."}, status=500)

    def create(self, request: HttpRequest) -> HttpResponse:
        payload, error_response = parse_json_body(request)
        if error_response is not None or payload is None:
            return error_response if error_response else JsonResponse({"error": "Invalid payload."}, status=400)

        name = payload.get("name")
        owner_roblox_user_id = payload.get("owner_roblox_user_id")
        display_name = payload.get("display_name")
        owner_server_id = payload.get("owner_server_id")

        if not isinstance(name, str) or not name.strip():
            return JsonResponse({"error": "Field 'name' must be a non-empty string."}, status=400)

        if isinstance(owner_roblox_user_id, bool) or not isinstance(owner_roblox_user_id, int):
            return JsonResponse({"error": "Field 'owner_roblox_user_id' must be an integer."}, status=400)
        
        if not isinstance(display_name, str) or not display_name.strip():
            return JsonResponse({"error": "Field 'display_name' must be a non-empty string."}, status=400)
        
        if not isinstance(owner_server_id, int) or not owner_server_id:
            return JsonResponse({"error": "Field 'owner_server_id' must be a non-empty string."}, status=400)
        
        session = self.service.create(
            name=name.strip(), 
            owner_roblox_user_id=owner_roblox_user_id, 
            display_name=display_name.strip(),
            owner_server_id=owner_server_id,
        )
        if session is None:
            return JsonResponse({"error": "Could not generate a unique session code."}, status=500)

        serialized_session = SessionSerializer(session)
        return JsonResponse(
            serialized_session.data,
            status=201,
        )

    def delete(self, request: HttpRequest, session_id: int) -> HttpResponse:
        payload, error_response = parse_json_body(request)
        if error_response is not None or payload is None:
            return error_response if error_response else JsonResponse({"error": "Invalid payload."}, status=400)
        
        if isinstance(session_id, bool) or not isinstance(session_id, int):
            return JsonResponse({"error": "Field 'session_id' must be an integer."}, status=400)
        
        try:
            deleted = self.service.delete(session_id=session_id)
            if not deleted:
                return JsonResponse({"error": "Session not found."}, status=404)
            return JsonResponse({"message": "Session deleted successfully."}, status=200)
        except Exception:
            return JsonResponse({"error": "Failed to delete session."}, status=500)
