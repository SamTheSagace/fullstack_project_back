from collections import defaultdict

from django.db import IntegrityError, transaction

from poker.helpers.utils import generate_session_code
from poker.models import MemberRole, MemberStatus, Session, SessionMember, SessionStatus
from .session_member_service import SessionMemberService

MAX_CODE_ATTEMPTS = 20


class SessionService:
    @staticmethod
    def create(name: str, owner_roblox_user_id: int, display_name: str) -> Session | None:
        for _ in range(MAX_CODE_ATTEMPTS):
            code = generate_session_code()
            try:
                with transaction.atomic():
                    session = Session.objects.create(
                        code=code,
                        name=name,
                        status=SessionStatus.WAITING,
                        owner_roblox_user_id=owner_roblox_user_id,
                    )
                    owner = SessionMemberService.create(
                        session=session,
                        roblox_user_id=owner_roblox_user_id,
                        display_name=display_name,
                        role=MemberRole.OWNER,
                    )
                    if owner is None:
                        raise IntegrityError(f"Failed to create session member for {display_name}")
    
                return session
            except IntegrityError:
                continue

        return None

    @staticmethod
    def list_waiting_with_members():
        sessions = list(
            Session.objects.filter(status=SessionStatus.WAITING).order_by("-created_at")
        )
        if not sessions:
            return []

        session_ids = [session.pk for session in sessions]
        members_by_session_id = defaultdict(list)

        members = SessionMember.objects.filter(session_id__in=session_ids).order_by("joined_at")
        for member in members:
            members_by_session_id[member.session_id].append(
                {
                    "id": member.pk,
                    "roblox_user_id": member.roblox_user_id,
                    "display_name": member.display_name,
                    "role": member.role,
                    "status": member.status,
                    "joined_at": member.joined_at.isoformat() if member.joined_at else None,
                }
            )

        payload = []
        for session in sessions:
            payload.append(
                {
                    "id": session.pk,
                    "code": session.code,
                    "name": session.name,
                    "status": session.status,
                    "owner_roblox_user_id": session.owner_roblox_user_id,
                    "created_at": session.created_at.isoformat() if session.created_at else None,
                    "updated_at": session.updated_at.isoformat() if session.updated_at else None,
                    "session_members": members_by_session_id.get(session.pk, []),
                }
            )

        return payload

    @staticmethod
    def delete(session_id: int) -> bool:
        deleted_count, _ = Session.objects.filter(pk=session_id).delete()
        return deleted_count > 0

    @staticmethod
    def get_by_code(code: str) -> Session | None:
        try:
            return Session.objects.get(code=code)
        except Session.DoesNotExist:
            return None
