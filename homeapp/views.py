from django.core.serializers import json
from django.shortcuts import render

from django.views.generic import ListView
from homeapp.models import Corporation, Department


# Create your views here.
def MainView(request):
    if request.method == 'GET':
        return render(request, 'homeapp/home.html')


class CorpView(ListView):
    model = Corporation
    context_object_name = 'corp_list'
    template_name = 'homeapp/corporation.html'


def DeptView(request):
    corp_name = request.GET.get('corp', None)
    dept_list = Department.objects.filter(corp_name=corp_name)
    context = {'dept_list': dept_list}
    return render(request, 'homeapp/department.html', context)