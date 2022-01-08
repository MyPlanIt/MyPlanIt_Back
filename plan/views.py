from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Plan, User_Plan
from .serializers import PlanSerializer, PlanDetailSerializer, UserPlanSerializer
from jwt_token import jwt_token


def get_user_and_plan(request, pk):
    res = list(jwt_token.get_token(request))
    user = res[0]  # 토큰으로 유저 조회
    plan = get_object_or_404(Plan, id=pk)
    return user, plan


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


# 특정 플랜 구매
class PlanBuyView(APIView):
    def post(self, request, pk):

        try:
            res = get_user_and_plan(request, pk)

            user_own_plan = User_Plan.objects.filter(user=res[0]).filter(plan=res[1]).filter(own_flag=True)
            user_plan = User_Plan.objects.filter(user=res[0]).filter(plan=res[1])

            if user_own_plan.exists():
                return Response({"message": "이미 구매한 플랜입니다."}, status=status.HTTP_400_BAD_REQUEST)

            elif user_plan.exists():
                user_plan.update(own_flag=True)
                return Response({"message": "구매 완료"}, status=status.HTTP_200_OK)

            else:
                new = User_Plan.objects.create(user=res[0], plan=res[1])
                new.save()
                return Response({"message": "구매 완료"}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 유저 소유 플랜 조회
class OwnPlanView(APIView):
    def get(self, request):

        try:
            res = list(jwt_token.get_token(request))
            user = res[0]  # 토큰으로 유저 조회
            user_plan = User_Plan.objects.filter(user=user).filter(own_flag=True)  # 토큰으로 조회한 유저의 own plan 저장
            serializer = UserPlanSerializer(user_plan, many=True).data

            plan_res = list()  # JSON 값 저장할 리스트 생성
            for i in range(len(serializer)):
                plan = serializer[i]
                own_plan = Plan.objects.filter(id=plan['plan'])
                own_plan_serializer = OwnPlanSerializer(own_plan, many=True).data
                plan_res.append(own_plan_serializer)

            return Response(plan_res, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
