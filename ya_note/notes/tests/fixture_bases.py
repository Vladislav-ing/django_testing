from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BasesTestSetup(TestCase):

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

        cls.login_url = reverse('users:login')
        cls.logout_url = reverse('users:logout')
        cls.signup_url = reverse('users:signup')
        cls.home_url = reverse('notes:home')

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

        cls.add_note_url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.notes_list_url = reverse('notes:list')
