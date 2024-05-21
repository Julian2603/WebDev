from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Article, Comment, Subscription
from .forms import CommentForm, SubscriptionForm
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
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
