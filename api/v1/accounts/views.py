from ast import If
import json
from urllib import response

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
from api.v1.accounts.serializers import LoginSerializer, OtpSerializer, RegisterSerializer, VerifySerializer
from api.v1.main.functions import generate_serializer_errors, validate_password
from main.decorators import check_mode, group_required
from main.encryption import *
from main.functions import generate_unique_id, get_auto_id, randomnumber, get_client_ip
from main.models import Country
from api.v1.main.functions import validate_password, generate_serializer_errors
from django.contrib.auth.hashers import make_password


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serialized = RegisterSerializer(data=request.data)
    if serialized.is_valid():
        username=request.data['username']
        phone = request.data['phone']
        password = request.data['password']
        name = request.data['name']
        ign = request.data['ign']
        email = request.data['email']
        country = request.data['country']
        ig_id = request.data['ig_id']
        if OtpRecord.objects.filter(phone=phone,is_applied=True).exists():
            if Country.objects.filter(country_code=country,is_active=True).exists():
                country_code=Country.objects.get(country_code=country,is_active=True)
                if not Profile.objects.filter(phone=phone).exists():
                    if not Profile.objects.filter(ig_id=ig_id).exists():
                        user = User.objects.create_user(
                            username=phone,
                            email=email,
                            password=password
                        )
                        encpt_password=encrypt(password)
                        profile = Profile.objects.create(
                            ign=ign,
                            ig_id=ig_id,
                            name=name,
                            user=user,
                            phone=phone,
                            email=email,
                            password=encpt_password,
                            is_verified=True,
                            country=country_code,
                        )
                        protocol = "http://"
                        headers = {
                            "Content-Type" : "application/json"
                        }
                        host = request.get_host()
                        data = {
                            "username" : phone,
                            "password" : password,
                        }
                        url = protocol + host + "/api/v1/accounts/token/"
                        response = requests.post(url, headers=headers, data=json.dumps(data))
                        print(response)
                        if response.status_code == 200:
                            response_data = {
                                "StatusCode": 6000,
                                "data": {
                                    "title": "Successful",
                                    "student_token" : response.json(),
                                }
                            }
                        
                        else:
                             response_data = {
                            "StatusCode" : 6001,
                            "data": {
                                "title" : "Failed",
                                "message" : "An error occurred"
                            }
                        }

                    else:
                        response_data={
                            'username already exist'
                        }
                else:
                    response_data={
                        'phone already registered'
                    }
        else:
            response_data={
                'verify phone first'
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


@api_view(['POST'])
@permission_classes((AllowAny,))
def send_otp(request):
    serialized=OtpSerializer(data=request.data)
    if serialized.is_valid():
        country_code=request.data['country']
        phone_number=request.data['phone']
        if Country.objects.filter(country_code=country_code,is_active=True).exists():
            country=Country.objects.get(country_code=country_code,is_active=True)
            if len(phone_number) == country.phone_number_length:
                if OtpRecord.objects.filter(phone=phone_number,is_applied=False).exists():
                    otprecord=OtpRecord.objects.get(phone=phone_number,is_applied=False)
                    if otprecord.attempts <= 3 :
                        response_data={
                            'otp': otprecord.otp
                        }
                    else:
                        response_data={
                            'limit exceed'
                        }
                else:
                    otp = randomnumber(4)
                    otp_record = OtpRecord.objects.create(
                        country = country,
                        phone = phone_number,
                        country_id = country.id,
                        otp = otp,
                    )
                    response_data={
                        'otp sent succecfully'
                    }
            else:
                response_data={
                    'not valid number'
                }
        else:
            response_data={
                'StatusCode':6001,
                'message':'not available in your country'
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


@api_view(['POST'])
@permission_classes((AllowAny,))
def verify_otp(request):
    serialized = VerifySerializer(data=request.data)
    if serialized.is_valid():
        phone_number = request.data['phone']
        country = request.data['country']
        otp_number=request.data['otp']
        if OtpRecord.objects.filter(phone=phone_number,is_applied=False,otp=otp_number).exists():
            otprecord=OtpRecord.objects.get(phone=phone_number,is_applied=False,otp=otp_number)
            otprecord.is_applied=True
            otprecord.save()
            response_data={
                'verified otp succesfully'
            }
        else:
            response_data={
                'already applied'
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


@api_view(['post'])
@permission_classes([AllowAny])
def login_user(request):
    serialized=LoginSerializer(data=request.data)
    if serialized.is_valid():
        username=request.data['username']
        password=request.data['password']
        if Profile.objects.filter(Q(phone=username) | Q(ig_id = username)).exists():
            profile = Profile.objects.get(Q(phone=username) | Q(ig_id = username))
            decr_password = decrypt(profile.password)
            phone=profile.phone
            if decr_password == password :
                protocol = "http://"
                headers = {
                    "Content-Type" : "application/json"
                }
                host = request.get_host()
                data = {
                    "username" : phone,
                    "password" : password,
                }
                url = protocol + host + "/api/v1/accounts/token/"
                response = requests.post(url, headers=headers, data=json.dumps(data))
                print(response)
                if response.status_code == 200:
                    response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "Successful",
                            "student_token" : response.json(),
                        }
                    }
                
                else:
                        response_data = {
                    "StatusCode" : 6001,
                    "data": {
                        "title" : "Failed",
                        "message" : "An error occurred"
                    }
                }
            else:
                response_data={
                    'incorrect password'
                }
        else:
            response_data={
                'no user found'
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