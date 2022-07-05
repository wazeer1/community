import json
import requests
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from mailqueue.models import MailerMessage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib


def generate_serializer_errors(args):
    message = ""
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        # message += "%s : %s | " %(key,error_message)
        message += f"{key} - {error_message} | "
    return message[:-3]


def validate_password(password):
    special_symbols =['$', '@', '#', '%', '!', '*', '?', '&']
    is_valid = True
    message = ""
    response_data = {}

    if len(password) < 8: 
        message = 'Password length should be at least 8!'
        is_valid = False
    elif len(password) > 20:
        message = 'Password length should not be greater than 20!'
        is_valid = False
    elif not any(char.isdigit() for char in password):
        message = 'Password should have at least one numeral'
        is_valid = False
    elif not any(char.isupper() for char in password):
        message = 'Password should have at least one uppercase letter'
        is_valid = False
    elif not any(char.islower() for char in password): 
        message = 'Password should have at least one lowercase letter'
        is_valid = False
    elif not any(char in special_symbols for char in password):
        message = 'Password should have at least one of the symbols ($, @, #, %, !, *, ?, &)'
        is_valid = False

    if is_valid:
        response_data = {
            "status" : True,
            "message" : "Success"
        }
    else:
        response_data = {
            "status" : False,
            "message" : message
        }
    
    return response_data


def get_current_profile(request):
    gender = ""
    email = ""
    campus = ""
    if Profile.objects.filter(user=request.user).exists():
        user_profile = get_object_or_404(Profile, user=request.user)
        if user_profile.email:
            email = user_profile.email
        
        title = "Success"
        
        response_data = {
            "StatusCode": 6000,
            "title": title,
            "user_profile_pk": user_profile.pk,
            "user_profile_data" : {
                "country" : user_profile.country.phone_code,
                "user_profile_pk" : user_profile.pk,
                "gender" : gender,
                "name" : user_profile.name,
                "email" : email,
                "phone" : user_profile.phone,
                "user_pk" : user_profile.user.pk,
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data" : {
                "title" : "Failed",
                "message" : "Profile not found",
            }
        }

    return response_data


def send_quick_fast2sms(phone, otp):
    API_KEY = "4Wt8UOn17uEJNapXFQRfmsLSg6TYBMV92ec0Zj5lhoCG3wzKvDfxTiU4NZDYJv1uk06AlpBz2PsgEaKr"
    SENDER_ID = "STPEDU"
    QT_TEMPLATE_ID = "126308"
    variable = "{#AA#}"

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = f"sender_id={SENDER_ID}&route=dlt&numbers={phone}&message={QT_TEMPLATE_ID}&variables_values={otp}&flash=0"
    
    headers = {
        'authorization': API_KEY,
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

    return True


def send_email(to_address, subject, content, html_content, attachment=None, attachment2=None, attachment3=None, bcc_address=None):
    new_message = MailerMessage()
    new_message.subject = subject
    new_message.to_address = to_address
    if bcc_address:
        new_message.bcc_address = bcc_address
    new_message.from_address = "Steyp Private Limited"
    new_message.content = content
    new_message.html_content = html_content
    if attachment:
        new_message.add_attachment(attachment)
    if attachment2:
        new_message.add_attachment(attachment2)
    if attachment3:
        new_message.add_attachment(attachment3)
    new_message.app = "default"
    new_message.save()


def create_student_activity(request, activity_pk, reference_pk, reference_app_name, reference_model_name):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : f"Bearer {token}"
    }

    data = {
        "reference_pk" : f"{reference_pk}",
        "reference_model_name" : reference_model_name,
        "reference_app_name" : reference_app_name,
    }

    protocol = "http://"
    if request.is_secure():
        protocol = "https://"

    host = request.get_host()

    url = protocol + host + f"/api/v1/activities/student-activity-create/{activity_pk}/"
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response = response.json()

    return response


def send_email(data, subject, message, to_address, file_name=""):
    # try:
    msg = MIMEMultipart()
    msg['From'] = data["from_address"]
    msg['To'] = to_address
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    if not file_name == "":
        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        attachment = open(file_name, "rb")
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % (file_name))

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

    server = smtplib.SMTP_SSL(data["server_ip"], data["server_port"])
    server.login(data["gmail_user"], data["gmail_password"])
    text = msg.as_string()
    server.sendmail(data["gmail_user"], to_address, text)
    server.quit()
    error = 0
    # except Exception as e:
    #     error = -1
    #     print(e)
