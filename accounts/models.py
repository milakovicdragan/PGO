from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.sessions.models import Session

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    pass



# Model to store the list of logged in users
class LoggedInUser(models.Model):
    #user can only have one entry in the table, there are no duplicate entries for a user in the table.
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE,)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
