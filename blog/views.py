# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from blog.serializers import *
from .models import *


class UsernameValidationView(CreateAPIView):
    serializer_class = ProfileSerializer
    allowed_methods = ["POST"]

    def post(self, request, *args, **kwargs):
        temp = request.data.get("username", None)
        if not temp:
            return Response({"msg": "no username"}, status=status.HTTP_400_BAD_REQUEST)

        q = User.objects.filter(username=temp)
        if q:
            return Response({"valid": "false"}, status=status.HTTP_409_CONFLICT)
        return Response({"valid": "true"}, status=status.HTTP_200_OK)


class SignupView(CreateAPIView):
    serializer_class = ProfileSerializer
    allowed_methods = ["POST"]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        name = request.data.get("name", None)
        phone = request.data.get("phone", None)
        email = request.data.get("email", None)

        if not username or not password or not name or not phone:
            return Response({"msg": "missing arguments"}, status=status.HTTP_400_BAD_REQUEST)

        tmp_user = User.objects.create_user(username=username)
        tmp_user.set_password(password)
        tmp_user.save()

        Token.objects.create(user=tmp_user)

        Profile.objects.create(user=tmp_user, name=name, phone=phone, email=email)

        return Response({"msg": "User Created"}, status=status.HTTP_201_CREATED)

