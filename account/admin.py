from django.contrib import admin

from .models import BusinessProfile, UserProfile


class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','created_at','state']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket']








admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
