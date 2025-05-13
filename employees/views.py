from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from employees.models import EmployerEmployee


# Create your views here.
@login_required
def employee_list(request):
    object_list = EmployerEmployee.objects.all()

    return render(request,
                  'employees/list.html',
                  {'employees': object_list})