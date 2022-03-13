from django.contrib import admin
from django.utils.html import mark_safe
from . import models

# Register your models here.


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.StackedInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (
        PhotoInline,
    )

    fieldsets = (
        (
            "Basic Info",
            {"fields": (
                "name", "description", "country", "city", "address", "room_type", "price",
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
        "count_amenities",
        "count_photos",
        "total_rating",
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

    raw_id_fields = (
        "host",
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

    def count_amenities(self, obj):
        return obj.amenities.count()

    # count_amenities.short_description = "Hello sexy"

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = "Photo Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):

        return mark_safe(f"<img width='50px' src='{obj.file.url}' />")

    get_thumbnail.short_description = "Thumbnail"
