from django.contrib import admin

from employees.models import EmployerEmployee


# Register your models here.
@admin.register(EmployerEmployee)
class EmployerEmployeeAdmin(admin.ModelAdmin):
    list_display = ('employer', 'employee',)
    list_filter = ('employer', 'employee',)

