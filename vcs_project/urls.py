from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from jobs import views as job_views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("accounts:login")),
    path('admin/', admin.site.urls),
    path("home/", job_views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),

    
    path("jobs/", include("jobs.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("profile/", include("profiles.urls")),
    path("training/", include("training.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("resume/", include("resume.urls")),
    path("notifications/", include("notifications.urls")),
    path("consultants/", include("consultants.urls")),
    path("session-notes/", include("session_notes.urls")),
    path("mock-interviews/", include("mock_interviews.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("redirect/", accounts_views.redirect_after_login, name="redirect_after_login"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
