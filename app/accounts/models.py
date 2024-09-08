from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Customized user model.

    Is needed in order to make it easier to customize User object later.
    """
    pass
