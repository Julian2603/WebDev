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