from django.db import models
from django.conf import settings

# Create your models here.
class EmployerEmployee(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee')

    class Meta:
        ordering = ('employee__last_name',)

    objects = models.Manager()
