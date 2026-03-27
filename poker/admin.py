from django.contrib import admin
from poker.models import Item, Session, Vote

from poker.models import Session, SessionMember, Item, Vote

# Register your models here.
admin.site.register(Session)
admin.site.register(SessionMember)
admin.site.register(Item)
admin.site.register(Vote)
