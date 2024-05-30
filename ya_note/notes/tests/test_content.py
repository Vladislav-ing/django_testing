from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note
from notes.tests.fixture_bases import BasesTestSetup

User = get_user_model()


class TestListNotes(BasesTestSetup):

    def test_notes_list_for_dif_users(self):
        client_status = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for custom_client, status in client_status:
            with self.subTest():
                response = custom_client.get(self.notes_list_url)
                status_search = self.note in response.context['object_list']
                self.assertEqual(status_search, status)


class TestFormAddEdit(BasesTestSetup):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Creator')
        cls.note = Note.objects.create(
            title='Заголовок', text='Текст заметки', author=cls.author
        )

    def test_edit_add_has_form_note(self):
        urls_args = (('notes:edit', (self.note.slug,)), ('notes:add', None))
        self.client.force_login(self.author)

        for url_name, args in urls_args:
            url = reverse(url_name, args=args)
            response = self.client.get(url)

            self.assertIn('form', response.context)

            self.assertIsInstance(response.context['form'], NoteForm)
