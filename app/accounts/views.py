import hashlib

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

User = get_user_model()


class LoginView(View):
    def post(self, request, *args, **kwargs):
        # Extract username and password from the request data
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=400)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login_template"))


class ChangePasswordView(LoginRequiredMixin, View):
    """Change user password while user is logged in.

    This view should be triggered from account page while user is logged in.
    There will be another flow for users that forgot their passwords and want to
    change it.
    """

    def post(self, request, *args, **kwargs):
        # Extract current password and new password from the request data
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if new_password1 != new_password2:
            return JsonResponse({"message": "Passwords do not match"}, status=400)

        validate_password(new_password1, user=request.user)

        request.user.set_password(new_password1)
        request.user.save()

        # Update the session to prevent the user from being logged out
        update_session_auth_hash(request, request.user)

        return JsonResponse({"message": "Password changed successfully"})


# class ResetPasswordView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         # Extract email from the request data
#         email = request.POST.get("email")
#
#         try:
#             user = User.objects.get(email=email, is_active=True)
#         except User.DoesNotExist:
#             return JsonResponse(
#                 {
#                     "message": (
#                         "If the user with this email exists, "
#                         "a password reset email will be sent."
#                     )
#                 }
#             )
#
#         # Generate a password reset token
#         token = default_token_generator.make_token(user)
#
#         # Create a password reset URL
#         reset_url = request.build_absolute_uri(
#             reverse(
#                 "accounts:password_reset_confirm",
#                 kwargs={
#                     "uid": "sha3_256:" + hashlib.sha3_256(user.pk).hexdigest(),
#                     "token": token,
#                 },
#             )
#         )
#
#         # Send password reset email
#         subject = "DeFi Swimmer - Password Reset Request"
#         message = f"Please click the following link to reset your password: {reset_url}"
#         send_mail(subject, message, "noreply@defi-swimmer.com", [email])
#
#         return JsonResponse(
#             {
#                 "message": (
#                     "If the user with this email exists, "
#                     "a password reset email will be sent."
#                 )
#             }
#         )


# class PasswordResetConfirmationView(View):
#     def get(self, request, *args, **kwargs):
#         # Extract uidb64 and token from the URL
#         uid = kwargs.get("uid")
#         token = kwargs.get("token")
#
#         try:
#             # Decode the user id
#             uid = urlsafe_base64_decode(uid).decode()
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#
#         # Check if the user exists and the token is valid
#         if user is not None and default_token_generator.check_token(user, token):
#             # Token is valid, render password reset form
#             return JsonResponse(
#                 {
#                     "message": "Password reset link is valid",
#                     "uid": uid,
#                     "token": token,
#                 }
#             )
#         else:
#             # Invalid link
#             return JsonResponse(
#                 {"message": "Password reset link is invalid or has expired"}, status=400
#             )


class ProtectedView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"message": f"This is a protected view for {request.user.username}"}
        )


class LoginPageTemplateView(TemplateView):
    template_name = "login_page.html"


class AccountTemplateView(TemplateView):
    template_name = "account_page.html"
