from django.urls import path

from . import views

app_name = "poker"

urlpatterns = [
    path("sessions/", views.sessions, name="sessions"),
    path("sessions/<int:id>/", views.delete_session, name="delete_session"),
    path("sessions/<str:code>/join/", views.join_session, name="join_session"),
    path("sessions/<str:code>/leave/", views.leave_session, name="leave_session"),
    path("session-members/create/", views.create_session_member, name="create_session_member"),
    path("sessions/<str:code>/items/", views.add_item, name="add_item"),
    path("sessions/<str:code>/start/", views.start_session, name="start_session"),
    path("sessions/<str:code>/vote/", views.vote_current_item, name="vote_current_item"),
    path("sessions/<str:code>/state/", views.get_session_state, name="get_session_state"),
    path("items/<int:id>/", views.get_item_by_id, name="get_item_by_id"),
    path("items/session/<int:id>/", views.get_item_by_session_id, name="get_item_by_session_id"),
    path("items/create/", views.create_item, name="create_item"),
    path("items/update/<int:id>/", views.update_item, name="update_item"),
    path("items/delete/<int:id>/", views.delete_item, name="delete_item"),
    path("votes/create/", views.create_vote, name="create_vote"),
    path("votes/update/<int:id>/", views.update_vote, name="update_vote"),
    path("votes/delete/<int:id>/", views.delete_vote, name="delete_vote"),
]
