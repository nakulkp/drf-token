from django.urls import path
from .views import (
    apiRegistration,
    apiTestToken
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'authapp'

urlpatterns = [
    path('register/', apiRegistration, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('test-token/', apiTestToken, name='test-token'),
]
