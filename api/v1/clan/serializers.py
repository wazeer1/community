from rest_framework import serializers
from accounts.models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class RegisterClanSerializer(serializers.Serializer):
    name = serializers.CharField()
    short_name = serializers.CharField()
    logo = serializers.FileField()
    squad_count = serializers.IntegerField()

    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',  
            'user',  
            'name',
            'ig_id',
            'ign', 
            'phone',
            'gender',
            'email', 
        ) 