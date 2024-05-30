from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BasesTestSetup(TestCase):
    notes_list_url = reverse('notes:list')
    TEXT_NOTE = 'Текст заметки'
    NEW_TEXT_NOTE = 'Новый текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Александр Пушкин')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title='Заголовок автора', text='Текст автора', author=cls.author
        )

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')
        cls.form_data = {'title': cls.note.title, 'text': cls.NEW_TEXT_NOTE}


class BasesLogiCreateSetup(TestCase):
    TITLE_NOTE = 'Заголовок записи'
    TEXT_NOTE = 'Текст записи'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='creator')
        cls.form_data = {'title': cls.TITLE_NOTE, 'text': cls.TEXT_NOTE}

        cls.create_note_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')

        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
