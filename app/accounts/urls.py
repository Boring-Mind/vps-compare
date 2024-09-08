from accounts.views import LoginView, LogoutView, ProtectedView, TestView
from django.urls import path

app_name = "accounts"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("test/", TestView.as_view(), name="test"),
    path("protected/", ProtectedView.as_view(), name="protected"),
]
