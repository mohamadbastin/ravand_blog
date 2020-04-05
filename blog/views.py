# Create your views here.

from django.utils.translation import ugettext_lazy as _
from rest_framework import parsers, renderers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

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


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        except serializers.ValidationError as e:
            try:
                a = str(e.detail['non_field_errors'][0])
                if a == _('Unable to log in with provided credentials.'):
                    return Response({"msg": "Unable to log in with provided credentials."},
                                    status=status.HTTP_404_NOT_FOUND)
            except KeyError:
                return Response({"msg": 'Must include "username" and "password".'},
                                status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        usr = self.request.user
        usr = Profile.objects.get(user=usr)
        try:
            title = request.data.get('title')
            content = request.data.get('content')
            cats = request.data.get('category')
        except:
            return Response({"msg": "wrong arguments"}, status=status.HTTP_400_BAD_REQUEST)

        tmp = Post.objects.create(title=title, content=content, author=usr)
        tmp.category.add(*cats)

        return Response({"msg": "created"}, status=status.HTTP_201_CREATED)


class PostListView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostRetrieveView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'ppk'
