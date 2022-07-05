from ipaddress import ip_address
import uuid

from django.db import models


DEVICE_REGISTER_EVENT_CHOICES = (
    ('login', 'Login'),
    ('signup', 'Signup'),
)


class Country(models.Model):
    name = models.CharField(max_length=128)
    web_code = models.CharField(max_length=128)
    country_code = models.CharField(max_length=128, blank=True, null=True)
    flag = models.ImageField(upload_to="countries/flags/",blank=True,null=True)
    phone_code = models.CharField(max_length=128,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    phone_number_length = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        db_table = 'main_country'
        verbose_name ='country'
        verbose_name_plural ='countries'
        ordering = ('name',)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=128)
    country = models.ForeignKey('main.Country', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'main_state'
        verbose_name ='state'
        verbose_name_plural ='states'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Mode(models.Model):
    readonly = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)
    down = models.BooleanField(default=False)

    class Meta:
        db_table = 'mode'
        verbose_name ='mode'
        verbose_name_plural ='mode'
        ordering = ('id',)

    def __str__(self):
        return str(self.id)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)
    creator = models.ForeignKey("auth.User", related_name="creator_%(class)s_objects", on_delete=models.CASCADE, null=True, blank=True)
    updater = models.ForeignKey("auth.User", related_name="updator_%(class)s_objects", on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# class Device(models.Model):
#     profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
#     date_added = models.DateTimeField(db_index=True,auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     register_event = models.CharField(max_length=128, choices=DEVICE_REGISTER_EVENT_CHOICES, null=True, blank=True)
#     is_ios_app = models.BooleanField(blank=True, null=True)
#     is_android_app = models.BooleanField(blank=True, null=True)
#     app_version = models.CharField(max_length=128, blank=True, null=True)
    
#     is_mobile = models.BooleanField(blank=True, null=True)
#     is_tablet = models.BooleanField(blank=True, null=True)
#     is_pc = models.BooleanField(blank=True, null=True)
#     browser_family = models.CharField(max_length=128, blank=True, null=True)
#     browser_version = models.CharField(max_length=128, blank=True, null=True)
#     os_family = models.CharField(max_length=128, blank=True, null=True)
#     os_version = models.CharField(max_length=128, blank=True, null=True)
#     device_family = models.CharField(max_length=128, blank=True, null=True)
    
#     ip_address = models.CharField(max_length=128, blank=True, null=True)
#     location = models.TextField(blank=True, null=True)

#     class Meta:
#         db_table = 'main_device'
#         verbose_name ='device'
#         verbose_name_plural ='devices'
#         ordering = ('id',)

#     def __str__(self):
#         return str(self.id)


class SlugBaseModel(models.Model):
    slug = models.SlugField(primary_key=True, max_length=128, blank=True)
    auto_id = models.PositiveIntegerField(db_index=True,unique=True)
    creator = models.ForeignKey("auth.User", related_name="creator_%(class)s_objects", on_delete=models.CASCADE, null=True, blank=True)
    updater = models.ForeignKey("auth.User", related_name="updator_%(class)s_objects", on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(db_index=True,auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)


    class Meta:
        abstract = True
