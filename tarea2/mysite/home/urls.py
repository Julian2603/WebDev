from django.urls import path
# from . import views
from . import views

urlpatterns = [
  path('', views.Home, name="home"),
  path('form/', views.Contact, name="contact")
]