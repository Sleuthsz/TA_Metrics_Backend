from django.urls import path

from slack_oauth.views import oauth_start, oauth_callback, logout

urlpatterns = [
    path('slack/install', oauth_start, name='oauth_start'),
    path('slack/oauth_redirect', oauth_callback, name='oauth_callback'),
    path('slack/logout', logout, name='logout')
]
