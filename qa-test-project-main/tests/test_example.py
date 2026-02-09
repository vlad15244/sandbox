"""
Пример теста - используйте как образец.
"""
import pytest
from model_bakery import baker
from rest_framework import status


@pytest.mark.django_db
class TestExample:

    def test_user_fixture_works(self, user):
        """Проверяет, что фикстура user работает."""
        assert user.username == 'testuser'

    def test_auth_client_works(self, auth_client, user):
        """Проверяет, что аутентифицированный клиент работает."""
        # Создаём урок для этого пользователя
        baker.make('lessons.Lesson', author=user, title='Test Lesson')

        response = auth_client.get('/api/lessons/')
        assert response.status_code == 200
        assert len(response.data) == 1

@pytest.mark.django_db
class TestLessonViewSet:
    def test_users_get_lessons(self, auth_client, lesson):
        """✅ Аутентифицированный пользователь получает список уроков"""
        response = auth_client.get('/api/lessons/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == lesson.id
        assert response.data[0]['title'] == lesson.title

    def test_get_lesson_by_id(self, auth_client, lesson):
        """✅ Аутентифицированный пользователь получает урок по ID"""
        response = auth_client.get(f'/api/lessons/{lesson.id}')  
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['id'] == lesson.id
        assert response.data[0]['title'] == lesson.title              
    




