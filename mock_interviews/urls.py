from django.urls import path
from . import views

app_name = "mock_interviews"

urlpatterns = [
    path("book/", views.book_mock_interview, name="book"),
    path("my/", views.my_mock_interviews, name="my_interviews"),
    path("complete/<int:interview_id>/",views.mark_interview_completed,name="mark_completed"),
    path("feedback/<int:interview_id>/",views.upload_feedback,name="upload_feedback"),
    path("consultant/", views.consultant_dashboard, name="consultant_dashboard"),
    path("assign/<int:interview_id>/",views.assign_mock_interview,name="assign_mock_interview"
)
    
]
