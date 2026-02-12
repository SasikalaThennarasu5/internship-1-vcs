from django.urls import path
from . import views
from .views import download_certificate

app_name = "training"

urlpatterns = [
    path("", views.training_home, name="home"),
    path("complete/<int:enrollment_id>/", views.complete_course, name="complete"),
    path("certificate/<int:enrollment_id>/", views.download_certificate, name="certificate"),
    path("my-courses/", views.my_courses, name="my_courses"),
     path("enroll/<int:course_id>/", views.enroll_course, name="enroll"),

]


