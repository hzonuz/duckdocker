from django.urls import path

from users.views import SignUp, Login, SignOut, UserView

app_name = "users"
urlpatterns = [
    path("signup/v0/", SignUp.as_view(), name="signup-v0"),
    path("login/v0/", Login.as_view(), name="login-v0"),
    path("signout/v0/", SignOut.as_view(), name="signout-v0"),
    path("me/v0/", UserView.as_view(), name="user-info-v0"),
]
