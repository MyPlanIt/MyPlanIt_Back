from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Plan, User_Plan, Proposal
from accounts.serializers import UserProposalSerializer


class PlanSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Plan
        exclude = ['price', 'main_img_url']


class PlanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'main_img_url']


class OwnPlanSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Plan
        fields = ['id', 'name', 'tags', 'writer_name', 'writer_img', 'writer_intro', 'intro_img_url', 'desc']


class UserPlanSerializer(serializers.ModelSerializer):
    plan = OwnPlanSerializer()

    class Meta:
        model = User_Plan
        fields = ['plan']


class ProposalSerializer(serializers.ModelSerializer):
    user = UserProposalSerializer()

    class Meta:
        model = Proposal
        fields = ['id', 'user', 'proposal']
