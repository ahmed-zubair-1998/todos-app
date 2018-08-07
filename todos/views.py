from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Todo

def index(request):
    todos_list = Todo.objects.order_by('-pub_date')
    context = {'todos_list': todos_list}
    template = loader.get_template('todos/index.html')
    return HttpResponse(template.render(context, request))
    #return render(request, 'todos/index', context)
