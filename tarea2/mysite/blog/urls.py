from django.urls import path
# from . import views
from .views import BlogView, ArticleDetailView
from . import views
urlpatterns = [
    # path('', views.blog, name="blog")
  path('articles', BlogView.as_view(), name="blog"),
  path('article/<int:pk>', ArticleDetailView.as_view(), name="article"),
  path('subscribe/', views.Subscribe, name="subscribe"),
  path('like-article/', views.like_article, name='like-article'),
  path('add_comment/', views.add_comment, name='add-comment'),
]