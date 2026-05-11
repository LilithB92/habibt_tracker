from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Сохраняет одну запись о курсе, связанную с:model:`habits.Habit`
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите Вашу почту")
    phone_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Телефон", help_text="Введите Ваш номер телефона"
    )
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватарка")
    country = models.CharField(
        max_length=60, blank=True, null=True, verbose_name="Страна", help_text="Введите Ваша страна"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
