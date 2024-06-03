from copy import deepcopy
from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.fixture_bases import BasesTestSetup

CORRECT_DATA_FORM = {
    'title': 'Новый заголовок заметки',
    'text': 'Новый текст заметки',
}


class TestCreateEditDeleteNote(BasesTestSetup):

    def test_anonymous_user_cant_create_note(self):
        count_notes_before = Note.objects.count()
        self.client.post(self.add_note_url, data=CORRECT_DATA_FORM)

        self.assertEqual((Note.objects.count() - count_notes_before), 0)

    def test_auth_user_can_create_note(self):
        set_notes_before = set(Note.objects.all())
        response = self.author_client.post(
            self.add_note_url, data=CORRECT_DATA_FORM
        )

        self.assertRedirects(response, self.success_url)

        set_notes_after = set(Note.objects.all()) ^ set_notes_before

        self.assertEqual(len(set_notes_after), 1)

        note_obj = set_notes_after.pop()

        self.assertEqual(note_obj.author, self.author)
        self.assertEqual(note_obj.title, CORRECT_DATA_FORM['title'])
        self.assertEqual(note_obj.text, CORRECT_DATA_FORM['text'])

    def test_twins_slugs_cant_create_by_note(self):
        set_slug_before = Note.objects.values_list('slug', flat=True)
        slug_note = slugify(CORRECT_DATA_FORM['title'][:100])

        self.assertNotIn(slug_note, set_slug_before)

        self.author_client.post(self.add_note_url, data=CORRECT_DATA_FORM)

        set_slug_after = Note.objects.values_list('slug', flat=True)

        self.assertIn(slug_note, set_slug_after)

        self.assertEqual((len(set_slug_after) - len(set_slug_before)), 1)

        response = self.author_client.post(
            self.add_note_url, data=CORRECT_DATA_FORM
        )

        self.assertCountEqual(
            Note.objects.values_list('slug', flat=True), set_slug_after
        )

        error = slug_note + WARNING
        self.assertFormError(
            response=response, form='form', field='slug', errors=error
        )

    def test_note_created_without_slug_equal_title(self):
        set_notes_before = set(Note.objects.all())

        self.assertNotIn('slug', CORRECT_DATA_FORM)

        self.author_client.post(self.add_note_url, data=CORRECT_DATA_FORM)
        set_notes_after = set(Note.objects.all())

        self.assertEqual(len(set_notes_before ^ set_notes_after), 1)

        note_obj = (set_notes_before ^ set_notes_after).pop()
        slug_note = slugify(CORRECT_DATA_FORM['title'][:100])

        self.assertEqual(slug_note, note_obj.slug)

    def test_author_user_can_delete_note(self):
        count_notes_before = Note.objects.count()
        note_obj = self.note

        self.assertIn(note_obj, Note.objects.all())

        response = self.author_client.delete(self.delete_url)

        self.assertRedirects(response, self.success_url)
        self.assertEqual((count_notes_before - Note.objects.count()), 1)
        self.assertNotIn(note_obj, Note.objects.all())

    def test_reader_user_cant_delete_note(self):
        count_notes_before = Note.objects.count()
        note_obj = self.note

        self.assertIn(note_obj, Note.objects.all())

        response = self.reader_client.delete(self.delete_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(count_notes_before, Note.objects.count())
        self.assertIn(note_obj, Note.objects.all())

    def test_author_user_can_edit_note(self):
        count_notes_before = Note.objects.count()
        self.assertIn(self.note, Note.objects.all())

        older_author = self.note.author

        response = self.author_client.post(
            self.edit_url, data=CORRECT_DATA_FORM
        )

        self.assertEqual(response['Location'], self.success_url)
        self.note.refresh_from_db()

        self.assertEqual(count_notes_before, Note.objects.count())

        self.assertIn(self.note, Note.objects.all())

        self.assertEqual(self.note.title, CORRECT_DATA_FORM['title'])
        self.assertEqual(self.note.text, CORRECT_DATA_FORM['text'])
        self.assertEqual(self.note.slug, slugify(
            CORRECT_DATA_FORM['title'][:100]))
        self.assertEqual(self.note.author, older_author)

    def test_reader_user_cant_edit_note(self):
        count_notes_before = Note.objects.count()
        self.assertIn(self.note, Note.objects.all())

        older_note = deepcopy(self.note)

        response = self.reader_client.post(
            self.edit_url, data=CORRECT_DATA_FORM
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()

        self.assertEqual(count_notes_before, Note.objects.count())

        self.assertIn(self.note, Note.objects.all())

        self.assertEqual(older_note.title, self.note.title)
        self.assertEqual(older_note.text, self.note.text)
        self.assertEqual(older_note.slug, self.note.slug)
        self.assertEqual(older_note.author, self.note.author)
