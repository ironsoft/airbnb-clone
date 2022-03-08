from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Message)
class MessagesAdmin(admin.ModelAdmin):

    """ Messages Admin Definition """

    list_display = (
        "__str__",
        "created",
    )


@admin.register(models.Conversation)
class ConversationsAdmin(admin.ModelAdmin):

    """ Conversations Admin Definition """

    list_display = (
        "__str__",
        "count_messages",
        "count_participants",
    )

    filter_horizontal = (
        "participants",
    )
