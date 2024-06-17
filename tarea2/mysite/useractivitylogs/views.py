from django.shortcuts import render
from .models import UserActionLog
from django.contrib.auth.decorators import login_required

@login_required
def action_log(request):
    user = request.user
    user_is_admin = user.is_authenticated and user.groups.filter(name='admin').exists()
    user_is_moderator = user.is_authenticated and user.groups.filter(name='moderator').exists()
    user_is_subscriber = user.is_authenticated and user.groups.filter(name='subscriber').exists()
    context = {
        'user_is_admin': user_is_admin,
        'user_is_moderator': user_is_moderator,
        'user_is_subscriber': user_is_subscriber,
    }
    logs = UserActionLog.objects.all().order_by('-timestamp')
    return render(request, 'action_log.html', {'logs': logs, 'context':context})
