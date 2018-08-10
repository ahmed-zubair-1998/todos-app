from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Todo


class IndexViewTests(TestCase):

    def login(self):
        self.user = User.objects.create_user('u7', 'miniso12')
        self.assertIs(self.client.login(username = 'u7', password = 'miniso12'),True)
    
    def test_login(self):
        self.user = User.objects.create_user('u7', 'miniso12')
        self.assertIs(self.client.login(username = 'u7', password = 'miniso12'),True)
        res = self.client.get(reverse('todos:index'))
        self.assertEqual(res.status_code, 200)

    def test_no_todo(self):
        self.login()
        res = self.client.get(reverse('todos:index'))
        self.assertContains(res, "No todo created")
        self.assertEqual(res.context['todos_list'], [])

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

        
        
