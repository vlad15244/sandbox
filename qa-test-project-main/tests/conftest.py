import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def user():
    """Создаёт обычного пользователя."""
    return baker.make('auth.User', username='testuser')


@pytest.fixture
def auth_client(user):
    """Аутентифицированный API клиент."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def lesson(db, user):
    """Урок для пользователя user"""
    return baker.make('lessons.Lesson', author = user, title = 'Test Lesson')

