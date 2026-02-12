from django.urls import path
from . import views

app_name = "consultants"

urlpatterns = [
    path("schedule/", views.schedule_session, name="schedule"),
    path("calendar/", views.my_calendar, name="calendar"),
    path("my-sessions/", views.my_sessions, name="my_sessions"),

]
