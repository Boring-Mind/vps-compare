from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView


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


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({"message": "Logout successful"})


class ProtectedView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"message": f"This is a protected view for {request.user.username}"}
        )


class TestView(TemplateView):
    template_name = "login_page.html"
