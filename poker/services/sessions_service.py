from collections import defaultdict
from typing import List

from django.db import IntegrityError, transaction

from poker.helpers.utils import generate_session_code
from poker.models import MemberRole, MemberStatus, Session, SessionMember, SessionStatus
from .session_member_service import SessionMemberService

MAX_CODE_ATTEMPTS = 20


class SessionService:
    @staticmethod
    def create(name: str, owner_roblox_user_id: int, display_name: str, owner_server_id: int) -> Session | None:
        for _ in range(MAX_CODE_ATTEMPTS):
            code = generate_session_code()
            try:
                with transaction.atomic():
                    session = Session.objects.create(
                        code=code,
                        name=name,
                        status=SessionStatus.WAITING,
                        owner_roblox_user_id=owner_roblox_user_id,
                        owner_server_id = owner_server_id,
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
    def list_waiting_with_members(owner_server_id: str) -> List[Session]:
        sessions = list(
                Session.objects.filter(status=SessionStatus.WAITING)
                .order_by("-created_at")
                .prefetch_related('members')
                .prefetch_related('items')
            )
        if owner_server_id:
            serv_id = int(owner_server_id)
            sessions = list(
                Session.objects.filter(status=SessionStatus.WAITING, owner_server_id=serv_id)
                .order_by("-created_at")
                .prefetch_related('members')
                .prefetch_related('items')
            )
        
        if not sessions:
            return []

        return sessions

    @staticmethod
    def delete(session_id: int) -> bool:
        deleted_count, _ = Session.objects.filter(pk=session_id).delete()
        return deleted_count > 0

    @staticmethod
    def get_by_code(code: str) -> Session | None:
        try:
            return Session.objects.prefetch_related('members').prefetch_related('items').get(code=code)
        except Session.DoesNotExist:
            return None
