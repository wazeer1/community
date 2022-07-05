from ast import If
import json
import profile
from urllib import response
from django.test import tag

import requests
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from yaml import serialize
from accounts.models import  OtpRecord, Profile
from api.v1 import clan
from api.v1.accounts.serializers import LoginSerializer, OtpSerializer, RegisterSerializer, VerifySerializer
from api.v1.clan.serializers import ProfileSerializer, RegisterClanSerializer
from api.v1.main.functions import generate_serializer_errors, get_current_profile, validate_password
from clan.models import Clan, ClanRequest, ClanSquad, ClanUser
from main.decorators import check_mode, group_required
from main.encryption import *
from main.functions import generate_unique_id, get_auto_id, randomnumber, get_client_ip
from main.models import Country
from api.v1.main.functions import validate_password, generate_serializer_errors
from django.contrib.auth.hashers import make_password



@api_view(['POST'])
def clan_register(request):
    serialized = RegisterClanSerializer(data=request.data)
    if serialized.is_valid():
        name=request.data['name']
        short_name=request.data['short_name']
        logo=request.data['logo']
        squad_count=request.data['squad_count']
        profile_data=get_current_profile(request)
        profile_data = profile_data["user_profile_data"]
        profile_pk=profile_data["user_profile_pk"]
        if Profile.objects.filter(pk=profile_pk).exists():
            profile=Profile.objects.get(pk=profile_pk)
            if Clan.objects.filter(name=name).exists():
                response_data={
                    'clan name already exists'
                }
            else:
                clan=Clan.objects.create(
                    name=name,
                    short_name=short_name,
                    logo=logo,
                    squad_count=squad_count,
                )
                clan_squad=ClanSquad.objects.create(
                    name='main squad',
                    member_count=5,
                    clan=clan,
                )
                clan_user=ClanUser.objects.create(
                    user=profile,
                    clan=clan,
                    is_admin=True,
                    squad=clan_squad,
                )
                response_data={
                    'clan created succecfully'
                }
        else:
            response_data={
                'no account'
            }
        
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def members_view(request,pk):
    if Profile.objects.filter(ig_id=pk).exists():
        instance=Profile.objects.get(ig_id=pk)
        serialized = ProfileSerializer(instance, context={"request": request})
        response_data={
            'hello world':serialized.data
        }
    else:
        response_data={
            'no data found'
        }
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['POST'])
def clan_request(request,pk):
    profile=get_current_profile(request)
    profile_data = profile["user_profile_data"]
    profile_pk=profile_data["user_profile_pk"]
    if Profile.objects.filter(id=profile_pk).exists():
        profile_current=Profile.objects.get(id=profile_pk)
        request_user=Profile.objects.get(pk=pk)
        if ClanUser.objects.filter(user=profile_current).exists():
            clan_user=ClanUser.objects.get(user=profile_current)
            if clan_user.is_admin == True:
                clan=clan_user.clan
                clan_request=ClanRequest.objects.create(
                    clan=clan,
                    user=request_user,
                )
                response_data={
                    'request send successfully'
                }
            else:
                response_data={
                    'you need to be admin'
                }
        else:
            {
                'you dont have any clans'
            }
    else:
        {
            'login required'
        }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_accept(request,pk):
    profile=get_current_profile(request)
    profile_data = profile["user_profile_data"]
    profile_pk=profile_data["user_profile_pk"]
    if Profile.objects.filter(id=profile_pk).exists():
        profile=Profile.objects.get(id=profile_pk)
        response_data={
            'thanks'
        }
    else:
        response_data={
            'you have no account'
        }
    return Response(response_data, status=status.HTTP_200_OK)