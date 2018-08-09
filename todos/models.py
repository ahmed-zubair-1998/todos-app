from django.db import models
from django.contrib.auth.models import User


    
class Todo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default = -1)
    todo_text = models.CharField(max_length = 2000)
    pub_date = models.DateTimeField('creation time')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.todo_text
