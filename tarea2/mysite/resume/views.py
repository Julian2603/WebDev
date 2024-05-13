from django.shortcuts import render

# Create your views here.
def Resume(request):
  return render(request, 'resume.html', {})