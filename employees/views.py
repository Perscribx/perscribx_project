from django.shortcuts import render

from employees.models import EmployerEmployee


# Create your views here.
def employee_list(request):
    object_list = EmployerEmployee.objects.all()

    return render(request,
                  'employees/list.html',
                  {'employees': object_list})