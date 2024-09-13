from accounts.views import (
    AccountTemplateView,
    ChangePasswordView,
    LoginPageTemplateView,
    LoginView,
    LogoutView,
    ProtectedView,
)
from django.urls import path

app_name = "accounts"
urlpatterns = [
    path("login-api/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path(
    #     "logout/",
    #     LogoutView.as_view(next_page="accounts:login_template"),
    #     name="logout",
    # ),
    path("login/", LoginPageTemplateView.as_view(), name="login_template"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("account/", AccountTemplateView.as_view(), name="account_template"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]
