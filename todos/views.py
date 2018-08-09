from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

from .models import Todo

@login_required
def index(request):
    if request.method == 'GET':
        todos_list = Todo.objects.filter(author=request.user).order_by('-pub_date')
        context = {'todos_list': todos_list}
        return render(request, 'todos/index.html', context)
    else:
        t_id = request.POST['todo_id']
        t = Todo.objects.get(id=t_id)
        t.status = True
        t.save()
        return HttpResponseRedirect(reverse('todos:index'))
        

@login_required
def new(request):
    if request.method == 'POST':
        text = request.POST.get('todo_text', False)
        t = Todo(author = request.user, todo_text = text, pub_date = timezone.now())
        t.save()
        return HttpResponseRedirect(reverse('todos:index'))
    else:
        return render(request, 'todos/new.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('todos:index'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
