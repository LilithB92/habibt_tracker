from django.conf import settings
from django.core import mail
from django.test import RequestFactory
from rest_framework.test import APITestCase

from users.services import EmailVerification


class AuthenticationByEmailTests(APITestCase):
    def setUp(self):
        # Создаем базовый запрос для генерации хоста в функции
        self.factory = RequestFactory()
        self.request = self.factory.get("/some-endpoint/")

        # Данные для теста
        self.token = "test-crypto-token-123"
        self.user_email = "user@example.com"

    def test_email_sent_successfully(self):
        """Проверка успешной отправки письма с верными данными"""
        EmailVerification.authentication_by_email(self.request, self.token, self.user_email)
        # Проверяем, что в виртуальный ящик упало ровно 1 письмо
        self.assertEqual(len(mail.outbox), 1)
        # Берем отправленное письмо для детального анализа
        sent_email = mail.outbox[0]
        # 1. Проверяем тему письма
        self.assertEqual(sent_email.subject, "Verify Your Email Address")
        # 2. Проверяем получателя
        self.assertEqual(sent_email.to, [self.user_email])
        # 3. Проверяем адрес отправителя (из settings)
        self.assertEqual(sent_email.from_email, settings.DEFAULT_FROM_EMAIL)
