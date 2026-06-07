from celery import shared_task
from django.core.mail import send_mail

from config import settings
from habits.models import Habit


@shared_task(bind=True)
def send_habit_email(self, habit_id):
    """
    Асинхронная задача для отправки писем подписчикам.
    """
    habit = Habit.objects.filter(pk=habit_id).first()
    subject = f"Напоминаем о привычке: {habit.action}"
    message = f"Ваша решение: {habit.__str__()}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[habit.user.email],  # Список адресов
        fail_silently=False,
    )
