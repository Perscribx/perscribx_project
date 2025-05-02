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
    priority = models.IntegerField()

    summary_pl = models.TextField()
    summary_en = models.TextField()
    summary_it = models.TextField()
    summary_de = models.TextField()
    summary_fr = models.TextField()
    summary_es = models.TextField()

    class Meta:
        ordering = ('priority',)

    def __str__(self):
        return self.title

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('notifications:summary_detail',
                       args=[self.date.year,
                             self.date.strftime('%m'),
                             self.date.strftime('%d'),
                             self.slug])
