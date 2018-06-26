from django.contrib import admin

from creche.models import Child, JournalEntry


class ChildAdmin(admin.ModelAdmin):
    """admin for Child."""

    pass


class JournalEntryAdmin(admin.ModelAdmin):
    """admin for JournalEntry."""

    pass


admin.site.register(Child, ChildAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)
