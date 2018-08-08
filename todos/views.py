from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Todo

@login_required
def index(request):
    todos_list = Todo.objects.filter(author=request.user).order_by('-pub_date')
    context = {'todos_list': todos_list}
    return render(request, 'todos/index.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        text = request.POST.get('todo_text', False)
        t = Todo(author = request.user, todo_text = text, pub_date = timezone.now())
        t.save()
        return HttpResponseRedirect(reverse('todos:index'))
    else:
        return render(request, 'todos/new.html')
