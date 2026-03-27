from django.utils import timezone

from poker.models import MemberRole, MemberStatus, Session, SessionMember, SessionStatus


class SessionMemberService:
    @staticmethod
    def list_all():
        return SessionMember.objects.all().order_by("-joined_at")

    @staticmethod
    def get_one_by_roblox_id(roblox_id: int):
        try:
            return SessionMember.objects.get(roblox_user_id=roblox_id)
        except SessionMember.DoesNotExist:
            return None

    @staticmethod
    def get_by_session_and_roblox_id(session: Session, roblox_user_id: int):
        try:
            return SessionMember.objects.get(session=session, roblox_user_id=roblox_user_id)
        except SessionMember.DoesNotExist:
            return None

    @staticmethod
    def create_or_get(
        roblox_user_id: int,
        display_name: str | None = None,
    ) -> SessionMember:
        member, _ = SessionMember.objects.get_or_create(
            roblox_user_id=roblox_user_id,
            defaults={
                "display_name": display_name,
                "role": MemberRole.GUEST,
                "status": MemberStatus.INACTIVE,
                "session": None,
            },
        )

        if display_name and member.display_name != display_name:
            member.display_name = display_name
            member.save(update_fields=["display_name", "updated_at"])

        return member

    @staticmethod
    def attach_to_session(
        member: SessionMember,
        session: Session,
        role: MemberRole = MemberRole.PLAYER,
        display_name: str | None = None,
    ):
        if session.status != SessionStatus.WAITING:
            return None

        member.session = session
        member.role = role
        member.status = MemberStatus.ACTIVE
        member.joined_at = timezone.now()
        member.left_at = None

        if display_name:
            member.display_name = display_name

        member.save()
        return member

    @classmethod
    def create(
        cls,
        session: Session | None,
        roblox_user_id: int,
        display_name: str | None,
        role: MemberRole = MemberRole.PLAYER,
    ):
        member = cls.create_or_get(roblox_user_id=roblox_user_id, display_name=display_name)
        if session is None:
            return member
        return cls.attach_to_session(member=member, session=session, role=role, display_name=display_name)

    @classmethod
    def join_session(
        cls,
        session_code: str,
        roblox_user_id: int,
        display_name: str | None = None,
        role: MemberRole = MemberRole.PLAYER,
    ):
        try:
            session = Session.objects.get(code=session_code)
        except Session.DoesNotExist:
            return None

        member = cls.create_or_get(roblox_user_id=roblox_user_id, display_name=display_name)
        return cls.attach_to_session(member=member, session=session, role=role, display_name=display_name)

    @classmethod
    def leave_session(cls, session_code: str, roblox_user_id: int):
        try:
            session = Session.objects.get(code=session_code)
        except Session.DoesNotExist:
            return False

        member = cls.get_by_session_and_roblox_id(session=session, roblox_user_id=roblox_user_id)
        if member is None:
            return False

        member.session = None
        member.role = MemberRole.GUEST
        member.status = MemberStatus.INACTIVE
        member.left_at = timezone.now()
        member.save()

        cls.delete_session_if_empty_or_owner_left(session=session, roblox_user_id=roblox_user_id)
        return True

    @staticmethod
    def delete(roblox_user_id: int):
        deleted_count, _ = SessionMember.objects.filter(roblox_user_id=roblox_user_id).delete()
        return deleted_count > 0

    @staticmethod
    def delete_session_if_empty_or_owner_left(session: Session, roblox_user_id: int) -> bool:
        has_members = SessionMember.objects.filter(session=session).exists()
        if not has_members:
            session.delete()
            return True
        if session.owner_roblox_user_id is not None and session.owner_roblox_user_id == roblox_user_id:
            session.delete()
            return True
        return False