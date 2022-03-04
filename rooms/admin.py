from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        (
            "Basic Info",
            {"fields": (
                "name", "description", "country", "address", "price",
            )},
        ),
        (
            "Times",
            {"fields": (
                "check_in", "check_out", "instant_book",
            )},
        ),
        (
            "Spaces",
            {"fields": (
                "guests", "beds", "bedrooms", "baths",
            )},
        ),
        (
            "More About the Space",
            {'classes': ('collapse',),
                "fields": (
                "amenities", "facilities", "house_rule",
            )},
        ),
        (
            "Last Details",
            {"fields": (
                "host",
            )},
        ),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
    )

    ordering = (
        "name",
        "price",
        "bedrooms",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rule",
        "city",
        "country",
    )

    search_fields = (
        "city",
        "host__username"
    )

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rule",
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
