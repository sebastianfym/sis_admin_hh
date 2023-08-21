import random
import smtplib

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import AnonymousUser
from .models import User


def get_access_token(user, request):
    token = str(RefreshToken.for_user(user).access_token)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def get_user_by_token(token: str):
    access_token_obj = AccessToken(token)
    user_id = access_token_obj['user_id']
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = AnonymousUser()
    return user