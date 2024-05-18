from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
# Create your views here.
# def blog(request):
#   return render(request, 'blog.html', {})

class BlogView(ListView):
  model = Article
  template_name = 'blog.html'

class ArticleDetailView(DetailView):
  model = Article
  template_name = 'article.html'

def Subscribe(request):
  return render(request, 'subscribe.html', {})

def like_article(request):
  article_id = request.POST.get('article_id')
  article = get_object_or_404(Article, id=article_id)
  article.likes += 1
  article.save()
  return JsonResponse({'likes': article.likes})