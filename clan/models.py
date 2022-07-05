from email import message
from unicodedata import name
import uuid
from django.db import models

# Create your models here.
class Clan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=155,blank=True,null=True)
    short_name = models.CharField(max_length=155,blank=True,null=True)
    logo = models.FileField(upload_to="clan-logo/",blank=True,null=True)
    coins = models.IntegerField(default=0,blank=True,null=True)
    clan_point = models.IntegerField(default=0,blank=True,null=True)
    squad_count = models.IntegerField(default=0,blank=True,null=True)

    class Meta:
        db_table = 'clan'
        verbose_name ='clan'
        verbose_name_plural ='clans'
        ordering = ('name',)
        
    def __str__(self):
        return self.name


class ClanSquad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=155,blank=True,null=True)
    member_count = models.IntegerField(blank=True,null=True)
    clan=models.ForeignKey('clan.Clan', on_delete=models.CASCADE)
    squad_head_id = models.CharField(max_length=155,blank=True,null=True)
    class Meta:
        db_table = 'squad'
        verbose_name ='squad'
        verbose_name_plural ='squads'
        ordering = ('name',)
        
    def __str__(self):
        return self.name


class ClanUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clan=models.ForeignKey('clan.Clan', on_delete=models.CASCADE)
    user=models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False)
    name=models.CharField(max_length=155,blank=True,null=True)
    squad = models.ForeignKey('clan.ClanSquad',on_delete=models.CASCADE)
    class Meta:
        db_table = 'clan_user'
        verbose_name ='clan_user'
        verbose_name_plural ='clan_users'
        ordering = ('name',)
        
    def __str__(self):
        return self.name


class ClanRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey('accounts.Profile',on_delete=models.CASCADE)
    clan=models.ForeignKey('clan.Clan',on_delete=models.CASCADE)
    message=models.CharField(max_length=155,blank=True,null=True,default='join our clan')
    class Meta:
        db_table = 'clan_request'
        verbose_name ='clan_request'
        verbose_name_plural ='clan_request'
    def __str__(self):
        return self.message