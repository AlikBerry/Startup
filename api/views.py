import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import MyUser, Friends, Wishes
from api.serializers import UserCreateSerializer, UserInfoSerializer, WishInfoSerializer


class Register(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = MyUser(
                full_name=serializer.data["full_name"],
                email=serializer.data["email"],
            )
            user.username = user.email
            user.set_password(serializer.data["password"])
            user.save()
            return JsonResponse({'Status': 'Ok', 'Message': 'Congratulation created', 'data': serializer.data},
                                status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestApiView(APIView):
    def get(self, *args, **kwargs):
        serializer = UserInfoSerializer(self.request.user)
        return JsonResponse(
            {"Status": "Ok", "data": serializer.data})


class FollowApiView(APIView):
    def post(self, *args, **kwargs):
        from_user = self.request.user
        to_user = MyUser.objects.filter(id=self.request.data.get('user_id')).last()
        follow_table = Friends.objects.filter(
            from_user=from_user,
            to_user=to_user
        ).last()
        if follow_table:
            follow_table.delete()
            return JsonResponse(
                {"Status": False,
                 "data": "unfollow"})
        if from_user and to_user:
            Friends.objects.create(
                from_user=from_user,
                to_user=to_user
            )
            return JsonResponse(
                {"Status": True,
                 "data": "follow"})



class WishListApiView(APIView):

    def get(self, *args, **kwargs):
        serializers = WishInfoSerializer(Wishes.objects.all(), many=True)
        return JsonResponse({
            "data": serializers.data
        })

# class WishCreate(APIView):
#
#     def post(self, request, *args, **kwargs):
#         serializer = WishInfoSerializer(data=request.data)
#         if serializer.is_valid():
#             wish = Wishes(
#                 content=serializer.data["content"],
#             )
#             wish.save()
#             return JsonResponse({'Status': 'Ok', 'Message': 'Congratulation created', 'data': serializer.data},
#                                 status=status.HTTP_201_CREATED)
#
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#


