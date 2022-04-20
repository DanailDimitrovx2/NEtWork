from django.urls import path
from .views import dashboard, profile_list, profile, register, login, logout_user

app_name = "socialNetWork"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout_user, name="logout"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
]