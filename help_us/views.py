from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

from .serializers import *


# Create your views here.


class WorkRequestCreateView(CreateAPIView):
    serializer_class = WorkRequestSerializer
    # parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        # def a(p):
        #     return request.data.get(p)

        serializer = WorkRequestSerializer(data=request.data)
        # serializer.is_valid()
        # print(serializer.errors)
        if serializer.is_valid():
            a = serializer.save()
            return Response({"msg": "done", "id": a.pk}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"msg", "something went wrong!"}, status=status.HTTP_409_CONFLICT)


class ResumeCreateView(CreateAPIView):
    serializer_class = ResumeSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = ResumeSerializer(data=request.data)

        if serializer.is_valid():
            a = serializer.save()
            b = WorkRequest.objects.get(pk=kwargs.get('id'))
            b.resumee = a
            b.save()
            return Response({"msg": "done"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"msg", "something went wrong!"}, status=status.HTTP_409_CONFLICT)
