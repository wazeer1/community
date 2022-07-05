from django.urls import path, re_path

from . import views

app_name = "api_v1_clan"


urlpatterns = [
    re_path(r'^clan/register/$', views.clan_register),
    re_path(r'^clan/add-members/(?P<pk>.*)/$', views.clan_request),
    re_path(r'^clan/view-members/(?P<pk>.*)/$', views.members_view),
    re_path(r'^clan/accept-clan/(?P<pk>.*)/$', views.user_accept),
]