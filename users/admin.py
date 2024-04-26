from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_phone', 'user_business_area', 'is_staff')
