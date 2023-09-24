from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import User
from apps.oauth2 import oauth2_sign_in
from apps.serializers import SignUpSerializers, SignInSerializers
from apps.tasks import send_to_gmail
from apps.token import get_tokens_for_user
from root import settings


class SignUpView(APIView):

    def post(self, requests, *args, **kwargs):
        serializers = SignUpSerializers(data=requests.data)
        serializers.is_valid(raise_exception=True)
        data = serializers.data
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError('Email alreadv exists!')
        user = User(**data)
        cache.set(f'user:{user.email}', user, timeout=settings.CACHE_TTL)
        send_to_gmail(data['email'])
        return Response({"success": "Code", "email": user.email})


class SignInView(APIView):

    def post(self, requests, *args, **kwargs):
        serializers = SignInSerializers(data=requests.data)
        serializers.is_valid(raise_exception=True)
        data = serializers.data
        user = User.objects.get(email=data['email'])
        return Response({"success": True, "email": user.email, "token": get_tokens_for_user(user)})


class SignInGoogle(APIView):

    def post(self, requests, *args, **kwargs):
        data = requests.data
        if token := data.get('token'):
            return Response(oauth2_sign_in(token))
        raise ValidationError('token is missing or invalid !')

# https://super-saver.onrender.com/media/insta?url=https%3A%2F%2Fwww.instagram.com%2Freel%2FCxaghJgt4kM%2F%3Futm_source%3Dig_web_copy_link
# https://www.instagram.com/reel/CxaghJgt4kM/?utm_source=ig_web_copy_link
# CxaghJgt4kM
# https://www.instagram.com/reel/CxdXS55MOys/?utm_source=ig_web_copy_link
