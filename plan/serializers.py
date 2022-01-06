from rest_framework import serializers
from .models import User_Plan
from taggit.serializers import (TaggitSerializer,
                                TagListSerializerField)


class OwnPlanSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = User_Plan
        fields = ['plan_id', 'plan_writer']