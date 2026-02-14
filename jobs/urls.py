from django.urls import path
from . import views

app_name = "jobs"   # 🔴 THIS LINE IS IMPORTANT

urlpatterns = [
    path("", views.job_list, name="list"),
    path("apply/<int:job_id>/", views.apply_job, name="apply"),
    path("save-job/<int:job_id>/", views.save_job, name="save_job"),
    path("saved-jobs/", views.saved_jobs, name="saved_jobs"),
    path("job/<int:pk>/", views.job_detail, name="job_detail"),
]
