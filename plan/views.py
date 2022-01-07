from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Plan
from .serializers import PlanSerializer, PlanDetailSerializer

# Create your views here.


# 전체 플랜 조회
class PlanView(APIView):
    def get(self, request):
        routine = Plan.objects.filter(category="Routine")
        growth = Plan.objects.filter(category="Growth")

        routine_serializer = PlanSerializer(routine, many=True).data
        growth_serializer = PlanSerializer(growth, many=True).data

        return Response({"Routine": routine_serializer,
                          "Growth": growth_serializer},
                        status=status.HTTP_200_OK)


# 특정 플랜 조회
class PlanDetailView(APIView):
    def get(self, request, pk, format=None):
        plan = get_object_or_404(Plan, id=pk)
        serializer = PlanDetailSerializer(plan)
        return Response(serializer.data)