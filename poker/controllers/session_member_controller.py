from django.http import HttpRequest, HttpResponse, JsonResponse

from poker.helpers.utils import parse_json_body
from poker.models import MemberRole
from poker.services.session_member_service import SessionMemberService

class SessionMemberController:
    def __init__(self):
        self.service = SessionMemberService()

    def list(self, request: HttpRequest) -> HttpResponse:
        try:
            session_members_payload = self.service.list_all()
            return JsonResponse({"session_members": session_members_payload}, status=200)
        except Exception:
            return JsonResponse({"error": "Failed to retrieve session members."}, status=500)

    def create(self, request: HttpRequest) -> HttpResponse:
        payload, error_response = parse_json_body(request)
        if error_response is not None or payload is None:
            return error_response if error_response else JsonResponse({"error": "Invalid payload."}, status=400)

        session_code = payload.get("session_code")
        roblox_user_id = payload.get("roblox_user_id")
        display_name = payload.get("display_name")
        role = payload.get("role", MemberRole.PLAYER)

        if not isinstance(session_code, str) or not session_code.strip():
            return JsonResponse({"error": "Field 'session_code' must be a non-empty string."}, status=400)

        if isinstance(roblox_user_id, bool) or not isinstance(roblox_user_id, int):
            return JsonResponse({"error": "Field 'roblox_user_id' must be an integer."}, status=400)

        if display_name is not None and not isinstance(display_name, str):
            return JsonResponse({"error": "Field 'display_name' must be a string."}, status=400)

        if role not in MemberRole.values:
            return JsonResponse({"error": f"Field 'role' must be one of: {', '.join(MemberRole.values)}."}, status=400)

        member = self.service.join_session(
            session_code=session_code.strip(),
            roblox_user_id=roblox_user_id,
            display_name=display_name.strip() if isinstance(display_name, str) and display_name.strip() else None,
            role=MemberRole(role),
        )
        if member is None:
            return JsonResponse({"error": "Failed to create session member for this session."}, status=400)

        return JsonResponse(
            {
                "id": member.pk,
                "session_id": member.session_id,
                "roblox_user_id": member.roblox_user_id,
                "display_name": member.display_name,
                "role": member.role,
                "status": member.status,
                "joined_at": member.joined_at.isoformat() if member.joined_at else None,
                "left_at": member.left_at.isoformat() if member.left_at else None,
            },
            status=201,
        )

    def join_session(self, request: HttpRequest) -> HttpResponse:
        payload, error_response = parse_json_body(request)
        if error_response is not None or payload is None:
            return error_response if error_response else JsonResponse({"error": "Invalid payload."}, status=400)

        effective_session_code = payload.get("session_code")
        roblox_user_id = payload.get("roblox_user_id")
        display_name = payload.get("display_name")
        role = payload.get("role", MemberRole.PLAYER)

        if not isinstance(effective_session_code, str) or not effective_session_code.strip():
            return JsonResponse({"error": "Field 'session_code' must be a non-empty string."}, status=400)

        if isinstance(roblox_user_id, bool) or not isinstance(roblox_user_id, int):
            return JsonResponse({"error": "Field 'roblox_user_id' must be an integer."}, status=400)

        if display_name is not None and not isinstance(display_name, str):
            return JsonResponse({"error": "Field 'display_name' must be a string."}, status=400)

        if role not in MemberRole.values:
            return JsonResponse({"error": f"Field 'role' must be one of: {', '.join(MemberRole.values)}."}, status=400)

        member = self.service.join_session(
            session_code=effective_session_code.strip(),
            roblox_user_id=roblox_user_id,
            display_name=display_name.strip() if isinstance(display_name, str) and display_name.strip() else None,
            role=MemberRole(role),
        )
        if member is None:
            return JsonResponse({"error": "Failed to join session. Please check the session code and try again."}, status=400)

        return JsonResponse(
            {
                "id": member.pk,
                "session_id": member.session_id,
                "roblox_user_id": member.roblox_user_id,
                "display_name": member.display_name,
                "role": member.role,
                "status": member.status,
                "joined_at": member.joined_at.isoformat() if member.joined_at else None,
                "left_at": member.left_at.isoformat() if member.left_at else None,
            },
            status=200,
        )

    def leave_session(self, request: HttpRequest) -> HttpResponse:
        payload, error_response = parse_json_body(request)
        if error_response is not None or payload is None:
            return error_response if error_response else JsonResponse({"error": "Invalid payload."}, status=400)

        effective_session_code = payload.get("session_code")
        roblox_user_id = payload.get("roblox_user_id")

        if not isinstance(effective_session_code, str) or not effective_session_code.strip():
            return JsonResponse({"error": "Field 'session_code' must be a non-empty string."}, status=400)

        if isinstance(roblox_user_id, bool) or not isinstance(roblox_user_id, int):
            return JsonResponse({"error": "Field 'roblox_user_id' must be an integer."}, status=400)

        success = self.service.leave_session(
            session_code=effective_session_code.strip(),
            roblox_user_id=roblox_user_id,
        )
        if not success:
            return JsonResponse({"error": "Failed to leave session. Please check the session code and try again."}, status=400)

        return JsonResponse({"message": "Left session successfully."}, status=200)
        
