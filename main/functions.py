import os
import random
import string
from random import randint

import requests
from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_unique_id(size=15, chars=string.ascii_lowercase + string.digits):
    
    return ''.join(random.choice(chars) for _ in range(size))


def generate_form_errors(args,formset=False):
    message = ''
    if not formset:
        for field in args:
            if field.errors:
                message += field.errors 
        for err in args.non_field_errors():
            message += str(err)
                
    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message +=field.errors
            for err in form.non_field_errors():
                message += str(err)
    return message


def get_auto_id(model):
    auto_id = 1
    latest_auto_id =  model.objects.all().order_by("-date_added")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id


def get_timezone(request):
    if "set_user_timezone" in request.session:
        user_time_zone = request.session['set_user_timezone']
    else:
        user_time_zone = "Asia/Kolkata"
    return user_time_zone


def get_current_role(request):
    is_superadmin = False
    is_student = False
    current_role = "user" 
    if request.user.is_authenticated():           
        groups = request.user.groups.all()
        if request.user.is_superuser:
            is_superadmin = True
        if groups.filter(name="student").exists():
            is_student = True
            
        if "current_role" in request.session:
            role =  request.session['current_role']
            if role == "administrator":
                current_role = "superadmin"
            elif is_student:
                current_role = "student"
        else:
            if is_superadmin:
                current_role = "superadmin"
            elif is_student:
                current_role = "student"    
        return current_role


def get_role(user):
    is_superadmin = False
    is_student = False
    role = "user" 
    if user.is_authenticated():           
        groups = user.groups.all()
        if user.is_superuser:
            is_superadmin = True
        if groups.filter(name="student").exists():
            is_student = True
            
        if is_superadmin:
            role = "superadmin"
        elif is_student:
            role = "student"
                    
        return role


def randomnumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
