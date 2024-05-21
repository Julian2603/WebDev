# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Article, Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST

class BlogView(ListView):
    model = Article
    template_name = 'blog.html'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article=self.object).order_by('-comment_date')
        context['form'] = CommentForm()
        return context
    
def Subscribe(request):
  return render(request, 'subscribe.html', {})

@require_POST
def like_article(request):
    article_id = request.POST.get('article_id')
    article = get_object_or_404(Article, id=article_id)
    article.likes += 1
    article.save()
    return JsonResponse({'likes': article.likes})

@require_POST
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        article_id = request.POST.get('article_id')
        comment.article = get_object_or_404(Article, id=article_id)
        comment.save()
        return JsonResponse({
            'name': comment.name,
            'comment_date': comment.comment_date.strftime('%Y-%m-%d'),
            'comment_body': comment.comment_body
        })
    return JsonResponse({'error': 'Invalid form submission'}, status=400)
