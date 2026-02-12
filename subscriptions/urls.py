from django.urls import path
from . import views

app_name = "subscriptions"

urlpatterns = [
    path("plans/", views.plan_select, name="plan_select"),
    path("free/", views.activate_free, name="activate_free"),
    path("payment/<str:plan>/", views.payment, name="payment"),
    path("payment-success/<str:plan>/", views.payment_success, name="payment_success"),
    path("success/", views.success, name="success"),
]
