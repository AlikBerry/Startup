from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, \
    verify_jwt_token

from api.views import Register, TestApiView
from . import views

app_name = "api"

urlpatterns = [
    path('token/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
    path('register/', Register.as_view()),
    path('test/', TestApiView.as_view()),
]