from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from useractivitylogs.models import UserActionLog


def login_page(request):
  UserActionLog.objects.create(user=request.user, action='login', details=f"loged in")
  return render(request, 'login.html')

def logout_view(request):
  UserActionLog.objects.create(user=request.user, action='logout', details=f"loged out")
  auth_logout(request)
  return redirect('/')

def login_view(request):
  UserActionLog.objects.create(user=request.user, action='login', details=f"loged in")
  return redirect('/login/')