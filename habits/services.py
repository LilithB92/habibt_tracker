import json
from datetime import timedelta
from django.utils import timezone

import requests
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from config import settings


class HabitPeriodicTask:
    """Класс для периодичных задач привычек"""

    @staticmethod
    def set_schedule(habit: object) -> object:
        """
        Установит график привычек
        :param habit: объект привычки
        :return: объект графики
        """
        task_time = habit.time.strftime("%H:%M").split(":")
        hour, minute = task_time[0], task_time[1]

        crontab_schedule, created = CrontabSchedule.objects.get_or_create(
            minute=minute, hour=hour, day_of_month=f"*/{habit.periodicity}"
        )
        return crontab_schedule

    @staticmethod
    def set_crontab(habit: object, crontab_schedule: object) -> None:
        """
        Устанавливает периодическую задачу

        :param habit: объект привычки
        :param crontab_schedule: объект графика
        :return: None
        """
        PeriodicTask.objects.create(
            crontab=crontab_schedule,
            name=f"{habit.action}",
            task="habits.tasks.send_habit_email",
            args=json.dumps([habit.pk]),
            expires=timezone.now() + timedelta(days=30),
        )


def send_tg_message(chat_id, message):
    """Отправляет сообщение телеграм боту"""
    url = f"{settings.TG_URL}{settings.TG_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=payload, timeout=80)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        return None
