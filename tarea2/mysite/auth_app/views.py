from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

def login_page(request):
  return render(request, 'login.html')

def logout_view(request):
  auth_logout(request)
  return redirect('/')

def login_view(request):
  return redirect('/login/')