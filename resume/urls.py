from django.urls import path
from . import views

app_name = "resume"

urlpatterns = [
    path("upload/", views.upload_resume, name="upload"),
    path("my/", views.my_resumes, name="my_resumes"),
]
