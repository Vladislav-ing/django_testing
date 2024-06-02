from http import HTTPStatus
from random import choice

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

CORRECT_DATA_FORM = {'text': 'Новый текст комментария'}

WRONG_DATA_FORM = {'text': f'Не верный текст, {choice(BAD_WORDS)}'}


def test_anonymous_cant_create_comment(client, detail_url):
    count_comments_before = Comment.objects.count()
    client.post(detail_url, data=CORRECT_DATA_FORM)

    assert count_comments_before == Comment.objects.count()


def test_author_can_create_comment(
    detail_url, author_client, author, news, comment_url
):
    comments_before = set(Comment.objects.all())
    response = author_client.post(detail_url, data=CORRECT_DATA_FORM)
    assertRedirects(response, comment_url)

    assert Comment.objects.count() == (len(comments_before) + 1)

    new_comment = set(Comment.objects.all()) ^ comments_before

    assert len(new_comment) == 1

    last_comment = new_comment.pop()

    assert last_comment.text == CORRECT_DATA_FORM['text']
    assert last_comment.author == author
    assert last_comment.news == news


def test_user_cant_use_badword_for_comment(detail_url, reader_client):
    count_comments_before = Comment.objects.count()
    response = reader_client.post(detail_url, data=WRONG_DATA_FORM)
    assertFormError(
        response=response, form='form', field='text', errors=WARNING
    )

    assert Comment.objects.count() == count_comments_before


def test_author_can_delete_comment(
    author_client, comment_url, delete_comment_url, comment
):
    count_comments_before = Comment.objects.count()
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, comment_url)

    assert Comment.objects.count() == (count_comments_before - 1)

    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_reader_cant_delete_comment(reader_client, delete_comment_url):
    count_comments_before = Comment.objects.count()
    response = reader_client.delete(delete_comment_url)

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert count_comments_before == Comment.objects.count()


def test_author_can_edit_comment(
    author_client, comment_url, comment, edit_comment_url
):
    count_comments_before = Comment.objects.count()
    response = author_client.post(edit_comment_url, data=CORRECT_DATA_FORM)
    assertRedirects(response, comment_url)

    assert Comment.objects.count() == count_comments_before

    update_comment = Comment.objects.get(pk=comment.pk)

    assert update_comment.text == CORRECT_DATA_FORM['text']
    assert update_comment.news == comment.news
    assert update_comment.author == comment.author


def test_reader_cant_edit_comment(reader_client, comment, edit_comment_url):
    count_comments_before = Comment.objects.count()
    response = reader_client.post(edit_comment_url, data=CORRECT_DATA_FORM)

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert count_comments_before == Comment.objects.count()

    update_comment = Comment.objects.get(pk=comment.pk)

    assert update_comment.text == comment.text
    assert update_comment.news == comment.news
    assert update_comment.author == comment.author
