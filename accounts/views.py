from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required")
            return redirect("/accounts/register/")

        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
            return redirect("/accounts/register/")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        user.first_name = name   # 👈 THIS IS IMPORTANT
        user.save()

        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend"
        )

        messages.success(request, "Account created successfully")
        return redirect("/subscriptions/plans/")


    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "accounts/login.html")

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def redirect_after_login(request):
    user = request.user

    if user.is_superuser:
        return redirect("/admin/")

    elif hasattr(user, "profile") and user.profile.role == "CONSULTANT":
        return redirect("consultants:dashboard")

    else:
        return redirect("home")   # 👈 Jobseeker goes to home
    
def root_redirect(request):
    return redirect("accounts:login")




