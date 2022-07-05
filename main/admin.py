from django.contrib import admin

from main.models import Country, Mode, State


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name','web_code','flag','phone_code','phone_number_length')
    search_fields = ('name', 'web_code')
admin.site.register(Country,CountryAdmin)


class StateAdmin(admin.ModelAdmin):
    list_display = ('name','country', 'is_active')

admin.site.register(State,StateAdmin)


class ModeAdmin(admin.ModelAdmin):
    list_display = ('down', 'maintenance', 'readonly')

admin.site.register(Mode,ModeAdmin)


