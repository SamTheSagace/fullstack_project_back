from django.urls import path

from . import views

app_name = "poker"

urlpatterns = [
    #Sessions
    path("sessions/", views.sessions, name="sessions"),
    path("sessions/<int:id>/", views.delete_session, name="delete_session"),
    path("sessions/<str:code>/join/", views.join_session, name="join_session"),
    path("sessions/<str:code>/leave/", views.leave_session, name="leave_session"),
    path("sessions/<int:session_id>/start/", views.start_session, name="start_session"),
    #Session members
    path("session-members/create/", views.create_session_member, name="create_session_member"),
    #Items
    path("items/<int:id>/", views.get_item_by_id, name="get_item_by_id"),
    path("items/session/<int:id>/", views.get_item_by_session_id, name="get_item_by_session_id"),
    path("items/create/", views.create_item, name="create_item"),
    path("items/update/<int:id>/", views.update_item, name="update_item"),
    path("items/delete/<int:id>/", views.delete_item, name="delete_item"),
    #Votes
    path("votes/create/", views.create_vote, name="create_vote"),
    path("votes/update/<int:id>/", views.update_vote, name="update_vote"),
    path("votes/delete/<int:id>/", views.delete_vote, name="delete_vote"),
]
