from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Todo


class IndexViewTests(TestCase):

    def login(self):
        self.user = User.objects.create_user('u7', 'miniso12')
        self.client.force_login(self.user)

    def test_login(self):
        #not logged-in
        res = self.client.get(reverse('todos:index'))
        self.assertEqual(res.status_code, 302)

        #logged-in
        self.login()
        res = self.client.get(reverse('todos:index'))
        self.assertEqual(res.status_code, 200)

    def test_no_todo(self):
        self.login()
        res = self.client.get(reverse('todos:index'))
        self.assertContains(res, "No todo created")
        tl = res.context['todos_list']
        self.assertEqual(len(res.context['todos_list']), 0)

    def test_todo_not_completed(self):
        self.login()
        t = Todo(author = self.user, todo_text = "test todo", pub_date = timezone.now())
        t.save()
        res = self.client.get(reverse('todos:index'))
        self.assertContains(res, "test todo")
        self.assertIs(b"Mark as done!" in res.content, True)

    def test_todo_completed(self):
        self.login()
        t = Todo(author = self.user, todo_text = "test todo", pub_date = timezone.now(), status= True)
        t.save()
        res = self.client.get(reverse('todos:index'))
        self.assertContains(res, "test todo")
        self.assertIs(b"Completed" in res.content, True)
