from django.urls import path, include
from .views import profile
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetView




urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile", profile, name="profile"),
    path("reset_auth", PasswordResetView.as_view(template_name="registration/reset.html"), name="reset_auth"),

]