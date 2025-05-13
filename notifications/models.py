from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class Summary(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, unique_for_date='date')
    url = models.URLField()
    priority = models.IntegerField(default=0, validators=(MinValueValidator(0), MaxValueValidator(2),))

    summary_pl = models.TextField()
    summary_en = models.TextField()
    summary_it = models.TextField()
    summary_de = models.TextField()
    summary_fr = models.TextField()
    summary_es = models.TextField()

    class Meta:
        ordering = ('-priority',)

    def __str__(self):
        return self.title

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('notifications:summary_detail',
                       args=[self.date.year,
                             self.date.strftime('%m'),
                             self.date.strftime('%d'),
                             self.slug])

class Task(models.Model):
    summary = models.ForeignKey('Summary', models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    percentage = models.IntegerField()
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('date',)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('notifications:task_detail',
                       args=[self.summary.date.year,
                           self.summary.date.strftime('%m'),
                           self.summary.date.strftime('%d'),
                           self.summary.slug,
                             self.slug])



