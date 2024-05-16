from django.shortcuts import render

# Create your views here.
def Home(request):
  return render(request, 'home.html', {})
def Contact(request):
  return render(request, 'contactme.html', {})