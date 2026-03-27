from django.db import models


class SessionStatus(models.TextChoices):
    WAITING = "waiting", "waiting"
    PLAYING = "playing", "playing"
    FINISHED = "finished", "finished"


class MemberRole(models.TextChoices):
    OWNER = "owner", "owner"
    PLAYER = "player", "player"
    GUEST = "guest", "guest"


class MemberStatus(models.TextChoices):
    ACTIVE = "active", "active"
    INACTIVE = "inactive", "inactive"


class ItemStatus(models.TextChoices):
    PENDING = "pending", "pending"
    VOTING = "voting", "voting"
    DONE = "done", "done"
    SKIPPED = "skipped", "skipped"


class Session(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.WAITING,
    )
    owner_roblox_user_id = models.BigIntegerField()
    current_item = models.ForeignKey(
        "Item",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_in_sessions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sessions"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["owner_roblox_user_id"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.code} ({self.status})"


class SessionMember(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.SET_NULL,
        related_name="members",
        null=True,
        blank=True,
    )
    roblox_user_id = models.BigIntegerField(unique=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=MemberRole.choices,
        default=MemberRole.PLAYER,
    )
    status = models.CharField(
        max_length=20,
        choices=MemberStatus.choices,
        default=MemberStatus.ACTIVE,
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "session_members"
        indexes = [
            models.Index(fields=["session"]),
            models.Index(fields=["roblox_user_id"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self) -> str:
        session_code = self.session.code if self.session else "no-session"
        return f"{self.display_name or self.roblox_user_id} in {session_code}"


class Item(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="items")
    created_by_roblox_user_id = models.BigIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    position = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=ItemStatus.choices,
        default=ItemStatus.PENDING,
    )
    final_value = models.CharField(max_length=255, null=True, blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "items"
        indexes = [
            models.Index(fields=["session"]),
            models.Index(fields=["session", "position"]),
            models.Index(fields=["session", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.session.code}#{self.position} {self.title}"


class Vote(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="votes")
    roblox_user_id = models.BigIntegerField()
    value = models.CharField(max_length=255)
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "votes"
        unique_together = (("item", "roblox_user_id"),)
        indexes = [
            models.Index(fields=["item"]),
            models.Index(fields=["roblox_user_id"]),
        ]

    def __str__(self) -> str:
        return f"{self.roblox_user_id} -> {self.value} ({self.item.pk})"
