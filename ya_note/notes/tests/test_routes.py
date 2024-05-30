from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.tests.fixture_bases import BasesTestSetup

User = get_user_model()


class TestRoutesPages(BasesTestSetup):

    def test_pages_availability(self):
        urls = ('notes:home', 'users:login', 'users:logout', 'users:signup')

        for path in urls:
            with self.subTest(path=path, msg=f'Не работает путь урлов {path}'):
                url = reverse(path)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_for_author_and_anonymous(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )

        urls_pk = (
            ('notes:edit', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for path, args in urls_pk:
                with self.subTest(user=user, path=path):
                    url = reverse(path, args=args)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_page_for_registration_user(self):
        urls_pk = (
            'notes:add',
            'notes:list',
            'notes:success',
        )

        self.client.force_login(self.author)
        for path in urls_pk:
            url = reverse(path)
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonimus_user(self):
        login_url = reverse('users:login')
        urls_args = (
            ('notes:edit', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:success', None),
            ('notes:list', None),
            ('notes:add', None),
        )

        for path, args in urls_args:
            with self.subTest(path=path):
                url = reverse(path, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
