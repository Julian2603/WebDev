from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class Article(models.Model):
  title = models.CharField(max_length=255)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.CharField(max_length=255, default="Category")
  date = models.DateField(default=datetime.date.today)
  abstract = models.CharField(max_length=500, default='Abstract of the article')
  reading_time = models.IntegerField(default=5)
  likes = models.IntegerField(default=0)
  body = models.TextField()

  def __str__(self):
    return self.title + ' | ' + str(self.author)
  
class Comment(models.Model):
  name = models.CharField(max_length=255)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  comment_date = models.DateField(default=datetime.date.today)
  comment_body = models.TextField()

  def __str__(self):
    return self.name + ' | ' + str(self.article.title)
  
class Subscription(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    FREQUENCY_CHOICES = [
        ('immediate', 'An email at the moment a new article gets published'),
        ('monthly', 'A monthly email regarding the summary of the month\'s new articles'),
    ]
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)

    def __str__(self):
        return self.name + ' | ' + self.email