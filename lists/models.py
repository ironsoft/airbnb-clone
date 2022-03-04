from django.db import models
from core import models as core_models

# Create your models here.


class List(core_models.TimeStampedModel):

    """ LIst Model Definition """

    name = models.CharField(max_length=80)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self) -> str:
        return self.name
