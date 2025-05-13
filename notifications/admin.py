from django.contrib import admin

from notifications.models import Summary, Task


# Register your models here.
@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'slug', 'url', 'priority', 'summary_pl', 'summary_en',
                    'summary_it', 'summary_de', 'summary_fr', 'summary_es',)
    list_filter = ('author', 'date',)
    search_fields = ('title', 'summary_pl', 'summary_en',
                    'summary_it', 'summary_de', 'summary_fr', 'summary_es',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    ordering = ('priority',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'date', 'percentage', 'description', 'slug',)
    list_filter = ('summary', 'date',)
    search_fields = ('title', 'description',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    ordering = ('date',)
    