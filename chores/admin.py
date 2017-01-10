from django.contrib import admin
from .models import (Chore, AssignedChores, Task)


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'frequency', 'value', 'active')
    list_editable = ('value', 'active')
    list_filter = ('frequency', 'active')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(AssignedChores)
class AssignedChoresAdmin(admin.ModelAdmin):
    filter_horizontal = ('chores',)
    list_display = ('user', 'possible_earnings_per_week', 'active_chores')


admin.site.register(Task)
