from django.shortcuts import render
from .models import UserActionLog
from django.contrib.auth.decorators import login_required

@login_required
def action_log(request):
    logs = UserActionLog.objects.all().order_by('-timestamp')
    return render(request, 'action_log.html', {'logs': logs})
