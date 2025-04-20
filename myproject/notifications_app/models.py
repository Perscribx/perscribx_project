from django.db import models

class SummaryEntry(models.Model):
    title = models.CharField(max_length=255)
    summary_pl = models.TextField(blank=True)
    summary_en = models.TextField(blank=True)
    summary_it = models.TextField(blank=True)
    summary_de = models.TextField(blank=True)
    summary_fr = models.TextField(blank=True)
    summary_es = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.author}"

    @classmethod
    def create_summary_entry(cls, title, author, department,
                              summary_pl="", summary_en="", summary_it="",
                              summary_de="", summary_fr="", summary_es="", data=None):
        entry = cls.objects.create(
            summary_pl=summary_pl,
            summary_en=summary_en,
            summary_it=summary_it,
            summary_de=summary_de,
            summary_fr=summary_fr,
            summary_es=summary_es,
            title=title,
            author=author,
            department=department,
            data=data
        )
        return entry

    @classmethod
    def check_record_by(cls, data):
        entries = SummaryEntry.objects.filter(data__date=data)
        
        if entries.exists():
            for entry in entries:
                return True

        else:
            return False
