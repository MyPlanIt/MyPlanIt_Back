from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Plan, Plan_todo, User_Plan


class PlanSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Plan
        exclude = ['price', 'intro_img_url']


class PlanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'intro_img_url']


class UserPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Plan
        fields = ['plan']


class OwnPlanSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Plan
        fields = ['id', 'name', 'tags', 'writer_name', 'intro_img_url']
