from django.conf import settings

import pytest

from news.forms import CommentForm


@pytest.mark.usefixtures('list_news')
def test_count_news_in_home(client, home_url):
    """Проверка количества объектов на гл. странице."""
    response = client.get(home_url)
    assert 'object_list' in response.context

    count_obj = response.context['object_list'].count()
    assert count_obj == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('list_news')
def test_order_news(client, home_url):
    """Проверка порядка объектов на гл. странице."""
    response = client.get(home_url)
    assert 'object_list' in response.context

    news_dates = [news.date for news in response.context['object_list']]
    sorted_dates = sorted(news_dates, reverse=True)
    assert news_dates == sorted_dates


@pytest.mark.usefixtures('list_comments')
def test_order_comments(client, detail_url):
    """Проверка порядка объектов комментариев на стр. новости."""
    response = client.get(detail_url)
    assert 'news' in response.context

    list_comments = response.context['news'].comment_set.all()
    comments_dates = [comment.created for comment in list_comments]
    sorted_comments = sorted(comments_dates)

    assert comments_dates == sorted_comments


def test_anonymous_hasnt_form_comment(client, detail_url):
    """Проверка наличия формы комментария для анонима на стр. новости."""
    response = client.get(detail_url)

    assert 'form' not in response.context


def test_user_has_form_comment(reader_client, detail_url):
    """Проверка наличия формы комментария для пользователя на стр. новости."""
    response = reader_client.get(detail_url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
