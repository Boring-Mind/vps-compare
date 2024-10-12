from django.db import models

class VPSProvider(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    # is_visible means if the provider is visible for our end customers on main page.
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "VPS Provider"
        verbose_name_plural = "VPS Providers"
        ordering = ['name']
