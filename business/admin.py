from django.contrib import admin

from business.models import Business, BusinessArea


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_title',)


@admin.register(BusinessArea)
class BusinessAreaAdmin(admin.ModelAdmin):
    list_display = ('business_area_title',)
