from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели «Пользователи».

    Обрабатывает преобразование экземпляров пользователи в формат JSON и выполняет валидацию
    входящие данные регистрации пользователи.
    """

    class Meta:
        model = User
        fields = ("id", "email", "phone_number", "avatar", "country", "password")


class UserGeneralInformationSerializer(ModelSerializer):
    """
    Сериализатор для модели «Пользователи», не для владельца.

    Обрабатывает преобразование экземпляров пользователи в формат JSON и выполняет  и выполняет валидацию
    входящие данные обновлении пользователи.
    """

    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "avatar",
            "country",
        )


class UserUpdateSerializer(ModelSerializer):
    """
    Сериализатор для обновленья модели «Пользователи».

    Обрабатывает преобразование экземпляров пользователи в формат JSON и выполняет просмотра данных.
    """

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("phone_number", "avatar", "country", "email", "password")

    def update(self, instance, validated_data):
        """Правильно обрабатывайте обновление паролей."""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)
