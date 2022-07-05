from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from accounts.models import  OtpRecord, Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_added', 'name', 'phone', 'ign', 'ig_id','email',
                    'country', 'otp_number', 'is_verified', 'password', 'gender', 'dob')
    ordering = ('-date_added',)
    search_fields = ('phone', 'pk', 'user__username', 'name')
    
admin.site.register(Profile,ProfileAdmin)


class OtpRecordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_added', 'phone',
                    'otp', 'attempts', 'is_applied')
    ordering = ('-date_added',)
    search_fields = ('phone', )

admin.site.register(OtpRecord, OtpRecordAdmin)