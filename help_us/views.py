from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

from .serializers import *


# Create your views here.


class WorkRequestCreateView(CreateAPIView):
    serializer_class = WorkRequestSerializer
    parser_classes = [FileUploadParser, MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        def a(p):
            return request.data.get(p)

        serializer = WorkRequestSerializer(data=request.data)
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "done"}, status=status.HTTP_201_CREATED)
        return Response({"msg", "something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)
