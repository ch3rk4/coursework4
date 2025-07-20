import pytest
import os
import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'


def pytest_configure():
    settings.DEBUG = False
    # Настройка базы данных для тестов
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    test_runner.setup_test_environment()


@pytest.fixture(scope='session')
def django_db_setup():
    """Настройка базы данных для тестов."""
    pass


@pytest.fixture
def api_client():
    """Фикстура для API клиента."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user():
    """Фикстура для пользователя."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Фикстура для аутентифицированного клиента."""
    api_client.force_authenticate(user=user)
    return api_client