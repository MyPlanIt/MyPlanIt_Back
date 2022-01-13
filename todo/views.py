from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from plan.models import Plan, User_Plan, Plan_todo, User_plan_todo
from .serializers import UserPlanTodoSerializer
from jwt_token import jwt_token
import datetime


# 해당 날짜의 플랜 투두 조회
class PlanTodoAPIView(APIView):
    def get(self, request, pk): # pk의 default = 현재 날짜 값 (ex, 20-01-11)
        User_plan_todo.objects.all().order_by('plan_id', 'plan_todo_id') # plan의 id값으로 1차 정렬 -> plan_todo_id로 2차 정렬
        try:
            res = list(jwt_token.get_token(request))
            user = res[0]  # 토큰으로 유저 조회
            plan_querysets = User_Plan.objects.filter(user=user) # User_Plan에서 user가 갖고 있는 plans들 가져오기

            data = {}

            for plan_queryset in plan_querysets: # 하나의 플랜에서 플랜 투두들 가져오기 위함
                plan = plan_queryset.plan # 플랜 가져오기
                plan_todo_querysets = User_plan_todo.objects.filter(user=user, date=pk, plan=plan) # user_plan_todo모델에서 해당 유저, 해당 날짜, 해당 플랜의 플랜투두들 가져오기
                serializer = UserPlanTodoSerializer(plan_todo_querysets, many=True) # serializer를 이용해 plan todo들을 가공된 Json data로 변환
                rate = plan_queryset.rate # 플랜의 달성률 가져오기
                serializer_data = list(serializer.data)
                serializer_data.insert(0, {'달성률': rate})
                data[plan_queryset.plan.name] = serializer_data # 딕셔너리 형태로 따로 만들기 (key: 플랜 이름, value: [ { 달성률 }, { 플랜투두1 }, { 플랜투두2 }, ... ])

            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 플랜 투두 완료 기능 (체크 기능)
class PlanTodoCheckAPIView(APIView):
   def post(self, request, plan_id, plan_todo_id):
       try:
           res = list(jwt_token.get_token(request))
           user = res[0] # 토큰으로 유저 조회
           user_plan_todo = get_object_or_404(User_plan_todo, id=plan_todo_id)

           if user_plan_todo.finish_flag == 0: # 미완료 -> 완료인 경우
               user_plan_todo.finish_flag = 1
           else: # user_plan_todo.finish_flag == 1 # 완료 -> 미완료 경우
               user_plan_todo.finish_flag = 0

           user_plan_todo.save()

           # 달성률 업데이트해주기
           user_plan = User_Plan.objects.filter(user=user, plan_id=plan_id)[0] # 해당 플랜
           user_plan_todos = User_plan_todo.objects.filter(user=user, plan_id=plan_id) # 해당 플랜의 투두들
           res = 0 # 누적합
           i = 0 # 투두 개수
           for user_plan_todo in user_plan_todos:
               res += user_plan_todo.finish_flag
               i += 1
           user_plan.rate = (res / i) * 100 # rate: 0 ~ 100 (% 단위로 표현)
           user_plan.save()
           return Response({"message": "success"}, status=status.HTTP_200_OK)
       except:
           return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


# 플랜 투두 내일하기 기능
class PlanTodoDelayAPIView(APIView):
    def post(self, request, plan_todo_id):
        try:
            user_plan_todo = get_object_or_404(User_plan_todo, id=plan_todo_id)
            user_plan_todo.date += datetime.timedelta(days=1) # 플랜 투두 날짜 + 1
            user_plan_todo.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)