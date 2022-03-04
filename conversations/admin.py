from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Conversation)
class ConversationsAdmin(admin.ModelAdmin):
    """ Conversations Admin Definition """
    pass


@admin.register(models.Message)
class MessagesAdmin(admin.ModelAdmin):
    """ Messages Admin Definition """
    pass
