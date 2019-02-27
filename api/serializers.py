from rest_framework import serializers

from api.forms import MyUserForm
from api.models import MyUser, BottleTarget, Bottle
from django.contrib.auth import authenticate


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'full_name', 'email', 'password')



class BottleInfo(serializers.ModelSerializer):
    class Meta:
        model = Bottle
        fields = ('id',  "content",
                  "url_image", "url_video",)


class UserFriends(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", 'full_name', "email")




class BottleTargetSerializer(serializers.ModelSerializer):
    target = UserFriends()
    class Meta:
        model = BottleTarget
        fields = ("target", "status", "next")


class BottleInfoSerializer(serializers.ModelSerializer):
    targets = BottleTargetSerializer(many=True)
    author = UserFriends()

    class Meta:
        model = Bottle
        fields = ("author", "content",
                  "url_image", "url_video", "targets")


class BottleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bottle
        fields = ("content",)


class UserInfoSerializer(serializers.ModelSerializer):
    friends = UserFriends(many=True)
    my_bottles = BottleInfoSerializer(many=True)
    incoming_bottles = BottleInfoSerializer(many=True)

    class Meta:
        model = MyUser
        fields = ('id', 'full_name', 'email', 'friends', 'my_bottles', 'incoming_bottles')
