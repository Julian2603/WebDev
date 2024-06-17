from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from useractivitylogs.models import UserActionLog
from .models import Article
@receiver(post_save, sender=Article)
def log_article_creation(sender, instance, created, **kwargs):
    if created:
        # Si se crea un nuevo artículo
        UserActionLog.objects.create(
            user=instance.author,  # Aquí debes ajustar según cómo almacenes al autor del artículo
            action='post_create',
            timestamp=timezone.now(),
            details=f"Created article {instance.id}"
        )
