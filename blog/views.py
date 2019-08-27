from django.shortcuts import render

# Create your views here.



def index(request):
    # user = Test('lijie', 30)
    # book_list = ['python', 'java', 'C++']
    # emps = Emp.objects.all()
    # return render(reg, 'index.html', {'title': 'Django', 'user': user, 'book_list': book_list, 'emps': emps})

    data = {'title': 'GET Form Submmit Page'}
    return render(request, 'index.html', data)

def result(request):
    if request.method == "POST":
        d = dict()
        d['name'] = request.POST['name']
        d['age'] = request.POST['age']
        return render(request, 'result.html', d)
