from django.db import models
from django_countries.fields import CountryField
from core import models as core_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """
    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey(
        "Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """
    name = models.CharField(max_length=140, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=140, null=True, blank=True)
    guests = models.IntegerField(null=True, blank=True)
    beds = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    baths = models.IntegerField(null=True, blank=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", default="", on_delete=models.CASCADE)
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField(
        "Facility", related_name="rooms", blank=True)
    house_rule = models.ManyToManyField(
        "HouseRule", related_name="rooms", blank=True)

    def __str__(self) -> str:
        return self.name
