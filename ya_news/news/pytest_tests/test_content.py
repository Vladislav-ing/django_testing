from django.conf import settings
from django.urls import reverse

import pytest

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('create_list_news')
def test_count_news_in_home(client):
    url = reverse('news:home')
    response = client.get(url)
    count_obj = response.context['object_list'].count()
    assert count_obj == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('create_list_news')
def test_order_news(client):
    url = reverse('news:home')
    response = client.get(url)
    news_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(news_dates, reverse=True)
    assert news_dates == sorted_dates


@pytest.mark.usefixtures('create_list_comments')
def test_order_comments(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)

    assert 'news' in response.context

    list_comments = response.context['news'].comment_set.all()
    comments_dates = [comment.created for comment in list_comments]
    sorted_comments = sorted(comments_dates)

    assert comments_dates == sorted_comments


@pytest.mark.parametrize(
    'user_client, has_form_comment',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    ),
)
def test_user_has_form_comment(user_client, has_form_comment, news):
    url = reverse('news:detail', args=(news.id,))
    response = user_client.get(url)

    assert ('form' in response.context) == has_form_comment

    if has_form_comment:
        assert isinstance(response.context['form'], CommentForm)
