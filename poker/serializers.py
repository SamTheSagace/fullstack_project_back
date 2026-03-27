from rest_framework import serializers
from poker.models import Item, Session, SessionMember, Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"

class ItemSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = "__all__"

class SessionMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionMember
        fields = "__all__"
        ordering = ['joined_at']

class SessionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    members = SessionMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = "__all__"