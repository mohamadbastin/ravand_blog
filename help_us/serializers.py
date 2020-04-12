from rest_framework import serializers

from .models import *


class WorkRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkRequest
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
