from datetime import timedelta

from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.tasks import send_habit_email
from users.models import User


class HabitAPITestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create(email="test@mail.ru")
        self.habit = Habit.objects.create(
            user=self.user, place="park", time="22:50:00", action="run", duration="00:01:20"
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        """Тестирование GET-запроса к API(просмотр список привычек)"""
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_details(self):
        """Тестирование GET-запроса к API(просмотр каждой привычки)"""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), self.habit.place)

    def test_habit_delete(self):
        """Тестирование DELETE-запроса к API(удаление привычки)"""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_create(self):
        """Тестирование POST-запроса к API(создание привычки)"""

        self.url = reverse("habits:habit-list")
        habit_dict = {
            "place": "park",
            "time": "22:50:00",
            "action": "learn foreign language",
            "duration": "00:01:20",
        }
        response = self.client.post(self.url, habit_dict)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["action"], "learn foreign language")
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """Тестирование Patch-запроса к API(обновление урока)"""
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        lesson_dict = {
            "place": "at home",
        }
        response = self.client.patch(url, lesson_dict)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "at home")


class TestHabitSerializer(APITestCase):
    """Тестирование валидации сериализатора HabitSerializer."""

    def setUp(self):
        # Базовый набор валидных данных для тестов
        self.valid_data = {
            "place": "Дома",
            "time": "08:00:00",
            "action": "Сделать зарядку",
            "is_pleasant": False,
            "periodicity": 1,
            "duration": timedelta(seconds=60),
            "is_public": True,
        }

    def test_valid_data_passes(self):
        """Проверка, что валидные данные успешно проходят валидацию."""
        serializer = HabitSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_pleasant_habit_with_reward_raises_error(self):
        """У приятной привычки не может быть вознаграждения."""
        data = self.valid_data.copy()
        data["is_pleasant"] = True
        data["reward"] = "Съесть яблоко"

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "У приятной привычки не может быть связанной привычки или вознаграждения.",
        )

    def test_duration_more_than_120_seconds_raises_error(self):
        """Время выполнения должно быть не более 120 секунд."""
        data = self.valid_data.copy()
        data["duration"] = timedelta(seconds=121)

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Время выполнения должно быть не более 120 секунд.",
        )

    def test_periodicity_more_than_7_days_raises_error(self):
        """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
        data = self.valid_data.copy()
        data["periodicity"] = 8

        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Нельзя выполнять привычку реже, чем 1 раз в 7 дней.",
        )

    def test_partial_update_without_duration_passes(self):
        """При частичном обновлении (без duration) не должно быть AttributeError."""
        # Передаем только одно поле, как при PATCH-запросе
        partial_data = {"action": "Новое действие"}
        serializer = HabitSerializer(data=partial_data, partial=True)
        self.assertTrue(serializer.is_valid())


class SendHabitEmailTaskTestCase(APITestCase):
    def setUp(self):
        """Настройка данных для тестов."""
        self.user = User.objects.create(email="testuser@example.com", password="password123")
        self.habit = Habit.objects.create(
            user=self.user,
            action="Сделать зарядку",
            place="park",
            time="06:50:00",
            duration="00:01:20",
        )

    def test_send_habit_email_success(self):
        """Успешный сценарий: письмо отправлено корректно."""
        # Вызываем задачу напрямую как обычную функцию (.delay() в тестах использовать не нужно)
        habit_id = self.habit.id
        send_habit_email(habit_id)
        # Проверяем, что в виртуальном почтовом ящике появилось одно письмо
        self.assertEqual(len(mail.outbox), 1)
        # Проверяем содержимое письма
        email = mail.outbox[0]
        self.assertIn("Напоминаем о привычке: Сделать зарядку", email.subject)
        self.assertEqual(email.to, ["testuser@example.com"])
