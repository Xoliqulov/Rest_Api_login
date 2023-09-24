from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import Serializer

from apps.models import User


class SignUpSerializers(Serializer):
    email = EmailField(max_length=255)
    password = CharField(max_length=255)
    confirm_password = CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password and confirm_password and password == confirm_password:
            attrs['password'] = make_password(password)
            return attrs
        else:
            raise ValidationError('invalid password !! ')


class SignInSerializers(Serializer):
    email = EmailField(max_length=255)
    password = CharField(max_length=255)

    def validate(self, attrs):
        password = attrs.pop('password')
        email = attrs.pop('email')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return user
        else:
            raise ValidationError('invalid password or email !')
