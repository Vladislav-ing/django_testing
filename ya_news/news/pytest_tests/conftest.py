from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

import pytest

from news.forms import BAD_WORDS
from news.models import Comment, News


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
def correct_form_data():
    form_data = {'text': 'Новый текст комментария'}
    return form_data


@pytest.fixture
def wrong_form_data():
    form_data = {'text': f'Не верный текст, {BAD_WORDS[0]}'}
    return form_data


@pytest.fixture
def id_news(news):
    return (news.id,)


@pytest.fixture
def id_comment(comment):
    return (comment.id,)


@pytest.fixture
def create_list_news():
    today = datetime.today()

    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        News.objects.create(
            title=f'Заголовок {index + 1}',
            text=f'Текст {index + 1}',
            date=today - timedelta(days=index),
        )


@pytest.fixture
def create_list_comments(author, news):
    actuall_time = timezone.now()

    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Текст {index + 1}'
        )
        comment.created = actuall_time - timedelta(days=index)
        comment.save()


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
