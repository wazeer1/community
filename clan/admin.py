from django.contrib import admin

from clan.models import Clan, ClanRequest, ClanSquad, ClanUser

# Register your models here.
class ClanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name')
    ordering = ('name',)
    search_fields = ('id', 'name')
    
admin.site.register(Clan,ClanAdmin)

class ClanUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id',)
admin.site.register(ClanUser,ClanUserAdmin)

class ClanSquadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id',)
admin.site.register(ClanSquad,ClanSquadAdmin)

class ClanRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')
    search_fields = ('id',)
admin.site.register(ClanRequest,ClanRequestAdmin)