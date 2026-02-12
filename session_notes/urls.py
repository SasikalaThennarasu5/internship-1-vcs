from django.urls import path
from . import views

app_name = "session_notes"

urlpatterns = [
    path("<int:session_id>/", views.view_session_notes, name="view"),
]
