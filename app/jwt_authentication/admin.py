from django.contrib import admin

from .models import JWTToken


class JWTTokenAdmin(admin.ModelAdmin):
    pass


admin.register(JWTToken, JWTTokenAdmin)
