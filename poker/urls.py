from django.urls import path

from . import views

app_name = "poker"

urlpatterns = [
    path("sessions/", views.sessions, name="sessions"),
    path("sessions/<str:code>/join/", views.join_session, name="join_session"),
    path("sessions/<str:code>/items/", views.add_item, name="add_item"),
    path("sessions/<str:code>/start/", views.start_session, name="start_session"),
    path("sessions/<str:code>/vote/", views.vote_current_item, name="vote_current_item"),
    path("sessions/<str:code>/state/", views.get_session_state, name="get_session_state"),
]
