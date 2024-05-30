from http import HTTPStatus

from django.contrib.auth import get_user_model

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.fixture_bases import BasesLogiCreateSetup, BasesTestSetup

User = get_user_model()


class TestCreationNote(BasesLogiCreateSetup):

    def test_create_note_for_anonimus_user(self):
        self.client.post(self.create_note_url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_create_note_for_auth_user(self):
        response = self.author_client.post(
            self.create_note_url, data=self.form_data
        )
        self.assertRedirects(response, self.success_url)

        count_notes = Note.objects.count()
        self.assertEqual(count_notes, 1)

        note_obj = Note.objects.get()
        self.assertEqual(self.author, note_obj.author)
        self.assertEqual(self.TITLE_NOTE, note_obj.title)
        self.assertEqual(self.TEXT_NOTE, note_obj.text)

    def test_cancel_create_note_for_second_twins_slug(self):
        self.author_client.post(self.create_note_url, data=self.form_data)
        response = self.author_client.post(
            self.create_note_url, data=self.form_data
        )
        error = slugify(self.form_data['title'])[:100] + WARNING
        self.assertFormError(
            response=response, form='form', field='slug', errors=error
        )

        count_notes = Note.objects.count()
        self.assertEqual(count_notes, 1)

    def test_create_note_without_slug(self):
        self.assertNotIn('slug', self.form_data)
        self.author_client.post(self.create_note_url, data=self.form_data)

        note_obj = Note.objects.get()
        title_to_slug = slugify(note_obj.title[:100])
        self.assertEqual(title_to_slug, note_obj.slug)


class TestEditDeleteNotes(BasesTestSetup):

    def test_delete_note_author_user(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)

        count_notes = Note.objects.count()
        self.assertEqual(count_notes, 0)

    def test_delete_note_reader_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        count_notes = Note.objects.count()
        self.assertEqual(count_notes, 1)

    def test_edit_note_author_user(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        success_response_url = response['Location']
        self.assertEqual(success_response_url, self.success_url)

        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_TEXT_NOTE)

    def test_edit_note_reader_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        self.note.refresh_from_db()
        self.assertNotEqual(self.note.text, self.NEW_TEXT_NOTE)
