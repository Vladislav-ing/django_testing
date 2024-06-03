from http import HTTPStatus

from notes.tests.fixture_bases import BasesTestSetup


class TestRoutesPages(BasesTestSetup):

    def test_pages_availabile_for_users(self):
        consent_status = HTTPStatus.OK
        failure_status = HTTPStatus.NOT_FOUND
        forwarding_status = HTTPStatus.FOUND

        urls_client_status = (
            (self.add_note_url, self.client, forwarding_status),
            (self.add_note_url, self.author_client, consent_status),
            (self.notes_list_url, self.client, forwarding_status),
            (self.notes_list_url, self.author_client, consent_status),
            (self.success_url, self.client, forwarding_status),
            (self.success_url, self.author_client, consent_status),
            (self.edit_url, self.client, forwarding_status),
            (self.edit_url, self.reader_client, failure_status),
            (self.edit_url, self.author_client, consent_status),
            (self.detail_url, self.client, forwarding_status),
            (self.detail_url, self.reader_client, failure_status),
            (self.detail_url, self.author_client, consent_status),
            (self.delete_url, self.client, forwarding_status),
            (self.delete_url, self.reader_client, failure_status),
            (self.delete_url, self.author_client, consent_status),
            (self.home_url, self.client, consent_status),
            (self.home_url, self.author_client, consent_status),
            (self.login_url, self.client, consent_status),
            (self.login_url, self.author_client, consent_status),
            (self.logout_url, self.client, consent_status),
            (self.logout_url, self.author_client, consent_status),
            (self.signup_url, self.client, consent_status),
            (self.signup_url, self.author_client, consent_status),
        )

        for url, custom_client, expect_status in urls_client_status:
            with self.subTest(url=url, custom_client=custom_client,
                              msg=f'Не работает путь {url}'):
                response = custom_client.get(url)
                self.assertEqual(response.status_code, expect_status)

    def test_anonymous_user_has_redirects(self):
        urls = (
            self.edit_url,
            self.detail_url,
            self.delete_url,
            self.success_url,
            self.notes_list_url,
            self.add_note_url,
        )

        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
