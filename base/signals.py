# base/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task

# When a task is created or updated
@receiver(post_save, sender=Task)
def task_saved(sender, instance, created, **kwargs):
    if created:
        print(f"🆕 Task Created: '{instance.title}' by {instance.user}")
    else:
        print(f"✏️ Task Updated: '{instance.title}' by {instance.user}")

# When a task is deleted
@receiver(post_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    print(f"🗑️ Task Deleted: '{instance.title}' by {instance.user}")
