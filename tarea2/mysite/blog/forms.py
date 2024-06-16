from django import forms
from .models import Comment, Subscription

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_body']

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'email', 'frequency']