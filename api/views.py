import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.models import MyUser
from api.serializers import UserCreateSerializer


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
    def get(self,*args, **kwargs):
        return JsonResponse(
            {"Status":"Ok", "Message":"Succesfully login username {}".format(self.request.user)})