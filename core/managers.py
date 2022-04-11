from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:  # 왜 models가 아니라 model이 되어야 하지?
            return None


class CustomUserManager(CustomModelManager, UserManager):
    pass
