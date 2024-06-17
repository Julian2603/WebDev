from django.contrib.auth.models import Group
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
from django.contrib import messages
from django.urls import reverse
from useractivitylogs.models import UserActionLog

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
        user = self.request.user
        user_is_admin = user.is_authenticated and user.groups.filter(name='admin').exists()
        user_is_moderator = user.is_authenticated and user.groups.filter(name='moderator').exists()
        user_is_subscriber = user.is_authenticated and user.groups.filter(name='subscriber').exists()

        context['user_is_admin'] = user_is_admin
        context['user_is_moderator'] = user_is_moderator
        context['user_is_subscriber'] = user_is_subscriber
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
        article = self.object  # El artículo actual

        user = self.request.user
        user_is_admin = user.is_authenticated and user.groups.filter(name='admin').exists()
        user_is_moderator = user.is_authenticated and user.groups.filter(name='moderator').exists()
        user_is_subscriber = user.is_authenticated and user.groups.filter(name='subscriber').exists()

        context['comments'] = Comment.objects.filter(article=article).order_by('-comment_date')
        context['form'] = CommentForm()
        context['user_is_admin'] = user_is_admin
        context['user_is_moderator'] = user_is_moderator
        context['user_is_subscriber'] = user_is_subscriber
        return context

    
def Subscribe(request):
    user = request.user
    user_is_admin = user.is_authenticated and user.groups.filter(name='admin').exists()
    user_is_moderator = user.is_authenticated and user.groups.filter(name='moderator').exists()
    user_is_subscriber = user.is_authenticated and user.groups.filter(name='subscriber').exists()
    context = {
        'user_is_admin': user_is_admin,
        'user_is_moderator': user_is_moderator,
        'user_is_subscriber': user_is_subscriber,
    }
    return render(request, 'subscribe.html', context)

@require_POST
@login_required
def like_article(request):
    article_id = request.POST.get('article_id')
    article = get_object_or_404(Article, id=article_id)
    article.likes += 1
    article.save()
    UserActionLog.objects.create(user=request.user, action='like', details=f"Liked article {article_id}")
    return JsonResponse({'likes': article.likes})

@require_POST
@login_required
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        article_id = request.POST.get('article_id')
        comment.article = get_object_or_404(Article, id=article_id)
        comment.name = f"{request.user.first_name} {request.user.last_name}" 
        comment.save()

        UserActionLog.objects.create(user=request.user, action='comment_add', details=f"Commented on article {article_id}")

        return JsonResponse({
            'name': comment.name,
            'comment_date': comment.comment_date.strftime('%Y-%m-%d'),
            'comment_body': comment.comment_body
        })
    return JsonResponse({'error': 'Invalid form submission'}, status=400)

def subscribe(request):
    user = request.user
    user_is_admin = user.is_authenticated and user.groups.filter(name='admin').exists()
    user_is_moderator = user.is_authenticated and user.groups.filter(name='moderator').exists()
    user_is_subscriber = user.is_authenticated and user.groups.filter(name='subscriber').exists()
    context = {
        'user_is_admin': user_is_admin,
        'user_is_moderator': user_is_moderator,
        'user_is_subscriber': user_is_subscriber,
    }
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            UserActionLog.objects.create(user=request.user, action='subscribe', details="Subscribed to the blog")
            # # Enviar correo de confirmación
            # send_mail(
            # 'Subscription Confirmation',
            # 'Thank you for subscribing to our blog!',
            # 'from@example.com',
            # [form.cleaned_data['email']],
            # fail_silently=False,
            # )

    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form, 'context': context})

def delete_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()

        UserActionLog.objects.create(user=request.user, action='comment_delete', details=f"Deleted comment {comment_id}")

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

def delete_article(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        article.delete()

        UserActionLog.objects.create(user=request.user, action='post_delete', details=f"Deleted article {article_id}")

        return JsonResponse({'status': 'success', 'redirect_url':reverse('blog')})
    return JsonResponse({'status': 'failed'}, status=400)

