from rest_framework import serializers

from api.forms import MyUserForm
from api.models import MyUser
from django.contrib.auth import authenticate


class UserCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = MyUser
        fields = ('full_name', 'email', 'password')

