from celery import shared_task
import time

@shared_task
def test_task():
    print("🟢 Celery test task started...")
    time.sleep(3)
    print("✅ Celery test task complete.")
