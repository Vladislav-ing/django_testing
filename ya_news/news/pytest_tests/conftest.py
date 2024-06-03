from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news, author=author, text='Текст комментария'
    )
    return comment


@pytest.fixture
def list_news():
    today = datetime.today()

    News.objects.bulk_create(
        News(
            title=f'Заголовок {index + 1}',
            text=f'Текст {index + 1}',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def list_comments(author, news):

    for index in range(10):
        Comment.objects.create(
            news=news, author=author, text=f'Текст {index + 1}'
        )


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_url(detail_url):
    return f'{detail_url}#comments'


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def home_url():
    return reverse('news:home')
