# Signals that fires when a user logs in and logs out

from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from accounts.models import LoggedInUser


@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))
    print("user loged in")
    print(LoggedInUser.objects.get_or_create(user=kwargs.get('user')))


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
    print("user loged out")
    print(LoggedInUser.objects.filter(user=kwargs.get('user')).delete())

