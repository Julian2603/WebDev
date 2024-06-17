from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActionLog


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActionLog.objects.create(user=user, action='login', timestamp=timezone.now(), details='User logged in')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserActionLog.objects.create(user=user, action='logout', timestamp=timezone.now(), details='User logged out')
