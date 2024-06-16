from django.urls import path
from . import views

urlpatterns = [
  path('action-log/', views.action_log, name='action_log'),
]
