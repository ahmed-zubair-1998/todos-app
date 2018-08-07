from django.db import models

class Todo(models.Model):
    todo_text = models.CharField(max_length = 2000)
    pub_date = models.DateTimeField('creation time')

    def __str__(self):
        return self.todo_text
