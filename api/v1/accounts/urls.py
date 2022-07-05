from django.urls import path, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

app_name = "api_v1_accounts"


urlpatterns = [
    re_path(r'^register/user/$', views.register),
    re_path(r'^send/otp/$', views.send_otp),
    re_path(r'^verify/otp/$', views.verify_otp),
    re_path(r'^login/user/$', views.login_user),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]