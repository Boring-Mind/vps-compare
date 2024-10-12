"""This app is meant to store and display all information about VPS providers."""
from django.apps import AppConfig


class VpsProvidersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vps_providers"
