from rest_framework import serializers

from api.forms import MyUserForm
from api.models import MyUser, Wishes, WishTarget
from django.contrib.auth import authenticate


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'full_name', 'email', 'password')



class WishInfo(serializers.ModelSerializer):
    class Meta:
        model = Wishes
        fields = ('id',  "content",
                  "url_image", "url_video",)


class UserFriends(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", 'full_name', "email")


class UserInfoSerializer(serializers.ModelSerializer):
    friends = UserFriends(many=True)
    my_wishes = WishInfo(many=True)
    incoming_wishes = WishInfo(many=True)

    class Meta:
        model = MyUser
        fields = ('id', 'full_name', 'email', 'friends', 'my_wishes', 'incoming_wishes')


class WishTargetSerializer(serializers.ModelSerializer):
    target = UserFriends()
    class Meta:
        model = WishTarget
        fields = ("target", "status", "next")


class WishInfoSerializer(serializers.ModelSerializer):
    user_id = WishTargetSerializer(many=True)
    author = UserFriends()

    class Meta:
        model = Wishes
        fields = ("author", "content",
                  "url_image", "url_video", "user_id")

