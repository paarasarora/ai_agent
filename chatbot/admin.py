from django.contrib import admin

from .models import Message,Conversation,FoodPreference


# class RatingAdmin(admin.ModelAdmin):
#     list_display = ["article", "rated_by", "value"]


admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(FoodPreference)