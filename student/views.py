from django.shortcuts import render
from student.models import Student
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    data = {
        'title': 'StutentManager',
        'name': 'name',
        'age': 'age'
    }
    return render(request, 'register.html', data)


def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        Student.objects.create(name=name, age=age)
        return HttpResponseRedirect('/')



def show(request):
    pass
