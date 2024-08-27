from django.shortcuts import render
from .models import MyModel
from .models import MongoModel

def my_view(request):
    data = MyModel.objects.all()
    return render(request, 'myapp/mytemplate.html', {'data': data})


def mongo_view(request):
    data = MongoModel.objects.using('mongo').all()
    return render(request, 'myapp/mongo_template.html', {'data': data})

