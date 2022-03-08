from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.List)
class ListsAdmin(admin.ModelAdmin):

    """ Lists Admin Difinition """

    list_display = (
        "name",
        "user",
        "count_rooms",
    )

    search_fields = (
        "name",
    )

    filter_horizontal = (
        "rooms",
    )
