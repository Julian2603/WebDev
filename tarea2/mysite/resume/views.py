from django.shortcuts import render

# Create your views here.
def Resume(request):
  user = request.user
  user_is_admin = user.is_authenticated and user.groups.filter(name='admin').exists()
  user_is_moderator = user.is_authenticated and user.groups.filter(name='moderator').exists()
  user_is_subscriber = user.is_authenticated and user.groups.filter(name='subscriber').exists()
  context = {
      'user_is_admin': user_is_admin,
      'user_is_moderator': user_is_moderator,
      'user_is_subscriber': user_is_subscriber,
  }
  return render(request, 'resume.html', context)