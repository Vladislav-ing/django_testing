from notes.forms import NoteForm
from notes.tests.fixture_bases import BasesTestSetup


class TestListFormNote(BasesTestSetup):

    def test_note_obj_send_on_list_notes(self):
        client_status = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for custom_client, status in client_status:
            with self.subTest(custom_client=custom_client, status=status):
                response = custom_client.get(self.notes_list_url)
                status_search = self.note in response.context['object_list']
                self.assertEqual(status_search, status)

    def test_form_note_send_on_add_or_edit_page(self):
        urls = (self.edit_url, self.add_note_url)

        for url in urls:
            response = self.author_client.get(url)

            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
