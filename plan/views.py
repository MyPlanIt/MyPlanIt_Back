from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Plan, User_Plan, Plan_todo, User_plan_todo
from .serializers import PlanSerializer, PlanDetailSerializer, UserPlanSerializer
from jwt_token import jwt_token
import datetime
from todo.views import get_user


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
class BuyPlanView(APIView):
    def post(self, request, pk):

        try:
            res = get_user_and_plan(request, pk)

            user_own_plan = User_Plan.objects.filter(user=res[0]).filter(plan=res[1]).filter(own_flag=True)
            user_plan = User_Plan.objects.filter(user=res[0]).filter(plan=res[1])

            if user_own_plan.exists():
                return Response({"message": "이미 구매한 플랜입니다."}, status=status.HTTP_208_ALREADY_REPORTED)

            elif user_plan.exists():
                user_plan.update(own_flag=True)
                return Response({"message": "구매 완료"}, status=status.HTTP_200_OK)

            else:
                new = User_Plan.objects.create(user=res[0], plan=res[1], own_flag=True)
                new.save()
                return Response({"message": "구매 완료"}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 특정 플랜 찜하기
class WishPlanView(APIView):
    def post(self, request, pk):

        try:
            res = get_user_and_plan(request, pk)

            user_wish_plan = User_Plan.objects.filter(user=res[0]).filter(plan=res[1]).filter(wish_flag=True)
            user_plan = User_Plan.objects.filter(user=res[0]).filter(plan=res[1])

            if user_wish_plan.exists():
                user_wish_plan.update(wish_flag=False)
                return Response({"message": "찜하기가 취소되었습니다."}, status=status.HTTP_200_OK)

            elif user_plan.exists():
                user_plan.update(wish_flag=True)
                return Response({"message": "찜!"}, status=status.HTTP_200_OK)

            else:
                new = User_Plan.objects.create(user=res[0], plan=res[1], wish_flag=True)
                new.save()
                return Response({"message": "찜!"}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 찜한 플랜 조회
class WishPlansView(APIView):
    def get(self, request):
        try:
            user_plan = User_Plan.objects.filter(user=get_user(request)).filter(wish_flag=True).order_by('created_at')

            if user_plan.exists():
                return Response(UserPlanSerializer(user_plan, many=True).data, status=status.HTTP_200_OK)

            else:
                return Response({"message": "찜한 플랜이 없습니다."}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 구매한 플랜 조회
class BuyPlansView(APIView):
    def get(self, request):
        try:
            user_plan = User_Plan.objects.filter(user=get_user(request)).filter(own_flag=True)  # 토큰으로 조회한 유저의 own plan 저장

            if user_plan.exists():
                return Response(UserPlanSerializer(user_plan, many=True).data, status=status.HTTP_200_OK)

            else:
                return Response({"message": "소유한 플랜이 없습니다."}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 이용 중 플랜 조회
class RegisteredPlanView(APIView):
    def get(self, request):
        try:
            user_plan = User_Plan.objects.filter(user=get_user(request)).filter(register_flag=True)

            if user_plan.exists():
                return Response(UserPlanSerializer(user_plan, many=True).data, status=status.HTTP_200_OK)

            else:
                return Response({"message": "이용 중인 플랜이 없습니다."}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 플랜 구매 -> 등록하기 (플랜에 해당하는 투두들 user_plan_todo db에 넣기)
class RegisterPlanView(APIView):
    def post(self, request, pk):  # pk : plan의 id값
        try:
            plan = get_object_or_404(Plan, id=pk)
            user_plan = get_object_or_404(User_Plan, user=get_user(request), plan=plan)

            if user_plan.register_flag:  # 이미 등록한 플랜인 경우
                return Response({"message": "이미 등록한 플랜입니다."}, status=status.HTTP_202_ACCEPTED)

            plan_todos = Plan_todo.objects.filter(plan=plan)
            date = datetime.date.today()  # 오늘 날짜 가져오기
            for plan_todo in plan_todos:
                date += datetime.timedelta(days=plan_todo.date)  # 날짜 + 걸리는 일수에 맞게 db에 넣어주기
                user_plan_todo = User_plan_todo(user=get_user(request), plan=plan, plan_todo=plan_todo, date=date)
                user_plan_todo.save()
            user_plan.register_flag = True  # 등록 flag = True 로 변경
            user_plan.save()
            return Response({"message": "등록완료"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "error"}, status=status.HTTP_202_ACCEPTED)


# 등록한 플랜 투두에서 제거하기 (User_Plan과 User_Plan_Todo에서 제거하기)
class DeletePlanView(APIView):
    def post(self, request, pk):  # pk : plan의 id값
        try:
            plan = get_object_or_404(Plan, id=pk)  # 지울 plan 가져오기
            user_plan = get_object_or_404(User_Plan, user=get_user(request), plan=plan)  # 지울 plan 가져오기

            if not user_plan.register_flag:  # 필요없을수도 있음
                return Response({"message": "이미 삭제한 플랜입니다."}, status=status.HTTP_202_ACCEPTED)

            user_plan.register_flag = False  # 등록 flag를 False로 변경
            user_plan.rate = 0  # 달성률 0으로 변경
            user_plan.save()

            User_plan_todo.objects.filter(user=get_user(request), plan=plan).delete()  # user_plan_todo에 등록된 객체들 다 삭제
            return Response({"message": "삭제완료"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "error"}, status=status.HTTP_202_ACCEPTED)
