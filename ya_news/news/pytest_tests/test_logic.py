from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_create_comment_for_anonymous(client, correct_form_data, detail_url):
    client.post(detail_url, data=correct_form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_create_comment_for_auth_user(
    correct_form_data, detail_url, reader_client, reader
):
    response = reader_client.post(detail_url, data=correct_form_data)
    assertRedirects(response, f'{detail_url}#comments')

    comments_count = Comment.objects.count()
    assert comments_count == 1

    comment_obj = Comment.objects.get()
    assert comment_obj.text == correct_form_data['text']

    assert comment_obj.author == reader


def test_cant_use_badword_for_comment(
    detail_url, reader_client, wrong_form_data
):
    response = reader_client.post(detail_url, data=wrong_form_data)
    assertFormError(
        response=response, form='form', field='text', errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
    author_client, comment_url, delete_comment_url
):
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, comment_url)

    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_reader_cant_delete_comment(reader_client, delete_comment_url):
    response = reader_client.delete(delete_comment_url)
    assert response.status_code == HTTPStatus.NOT_FOUND

    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
    author_client, comment_url, comment, correct_form_data, edit_comment_url
):
    response = author_client.post(edit_comment_url, data=correct_form_data)
    assertRedirects(response, comment_url)

    comment.refresh_from_db()
    assert comment.text == correct_form_data['text']


def test_reader_cant_edit_comment(
    reader_client, comment, correct_form_data, edit_comment_url
):
    response = reader_client.post(edit_comment_url, data=correct_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND

    comment.refresh_from_db()
    assert comment.text != correct_form_data['text']
