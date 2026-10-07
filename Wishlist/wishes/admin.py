from django.contrib import admin

from .models import Wish


@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ("text", "date", "done", "user")
    list_filter = ("done", "date")
    search_fields = ("text",)
