from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Article, Comment, Subscription
from .forms import CommentForm, SubscriptionForm
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Article

class BlogView(ListView):
    model = Article
    template_name = 'blog.html'
    context_object_name = 'articles'
    paginate_by = 5  # Default pagination

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'date')
        count = int(self.request.GET.get('count', self.paginate_by))
        query = self.request.GET.get('query', '')

        if query:
            filtered_articles = Article.objects.filter(title__icontains=query)
        else:
            filtered_articles = Article.objects.all()

        if order_by == 'likes':
            filtered_articles = filtered_articles.order_by('-likes')
        else:
            filtered_articles = filtered_articles.order_by('-date')

        return filtered_articles[:count]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_by = self.request.GET.get('order_by', 'date')
        count = int(self.request.GET.get('count', self.paginate_by))
        query = self.request.GET.get('query', '')

        if query:
            filtered_articles = Article.objects.filter(title__icontains=query)
        else:
            filtered_articles = Article.objects.all()

        if order_by == 'likes':
            filtered_articles = filtered_articles.order_by('-likes')
        else:
            filtered_articles = filtered_articles.order_by('-date')

        filtered_articles = filtered_articles[:count]

        remaining_articles = Article.objects.exclude(id__in=filtered_articles.values_list('id', flat=True))

        context['filtered_articles'] = filtered_articles
        context['remaining_articles'] = remaining_articles
        context['order_by'] = order_by
        context['count'] = count
        context['query'] = query
        return context


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
@login_required
def like_article(request):
    article_id = request.POST.get('article_id')
    article = get_object_or_404(Article, id=article_id)
    article.likes += 1
    article.save()
    return JsonResponse({'likes': article.likes})

@require_POST
@login_required
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

def subscribe(request):
  if request.method == 'POST':
    form = SubscriptionForm(request.POST)
    if form.is_valid():
      form.save()
      # Enviar correo de confirmación
      send_mail(
        'Subscription Confirmation',
        'Thank you for subscribing to our blog!',
        'from@example.com',
        [form.cleaned_data['email']],
        fail_silently=False,
      )
  else:
    form = SubscriptionForm()
  return render(request, 'subscribe.html', {'form': form})
