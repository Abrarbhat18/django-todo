from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Task)
def task_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"🟢 Task created: '{instance.title}' (user: {instance.user})")
        # Example: Send email here or log to a file
    else:
        print(f"📝 Task updated: '{instance.title}'")
