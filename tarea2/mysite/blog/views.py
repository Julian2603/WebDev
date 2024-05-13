from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
# Create your views here.
# def blog(request):
#   return render(request, 'blog.html', {})

class BlogView(ListView):
  model = Article
  template_name = 'blog.html'

class ArticleDetailView(DetailView):
  model = Article
  template_name = 'article.html'