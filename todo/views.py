from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from plan.models import Plan, User_Plan, Plan_todo, User_plan_todo
from .serializers import UserPlanTodoSerializer
from jwt_token import jwt_token
import datetime


class PlanTodoAPIView(APIView):
    def get(self, request, pk): # pk의 default = 현재 날짜 값 (ex, 20-01-11)
        User_plan_todo.objects.all().order_by('plan_id', 'plan_todo_id') # plan의 id값으로 1차 정렬 -> plan_todo_id로 2차 정렬
        try:
            res = list(jwt_token.get_token(request))
            user = res[0]  # 토큰으로 유저 조회
            plan_querysets = User_Plan.objects.filter(user=user)

            data = {}

            for plan_queryset in plan_querysets:
                plan = plan_queryset.plan
                plan_todo_querysets = User_plan_todo.objects.filter(user=user, date=pk, plan=plan)
                serializer = UserPlanTodoSerializer(plan_todo_querysets, many=True)
                rate = plan_queryset.rate # 달성률
                serializer_data = list(serializer.data)
                serializer_data.insert(0, {'달성률': rate})
                data[plan_queryset.plan.name] = serializer_data

            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


class PlanTodoCheckAPIView(APIView):
   def post(self, request, plan_id, plan_todo_id):
       try:
           print(plan_todo_id)
           print(type(plan_todo_id))
           res = list(jwt_token.get_token(request))
           user = res[0] # 토큰으로 유저 조회
           user_plan_todo = get_object_or_404(User_plan_todo, id=plan_todo_id)

           print(user_plan_todo)
           print(user_plan_todo.finish_flag)
           if user_plan_todo.finish_flag == 0: # 미완료 -> 완료인 경우
               print("hi")
               user_plan_todo.finish_flag = 1
               user_plan_todo.save()

               user_plan = User_Plan.objects.filter(user=user, plan_id=plan_id)[0]
               print(user_plan)

               user_plan_todos = User_plan_todo.objects.filter(user=user, plan_id=plan_id)
               res = 0
               i = 0
               for user_plan_todo in user_plan_todos:
                   res += user_plan_todo.finish_flag
                   i += 1
               user_plan.rate = (res/i)*100
               user_plan.save()

               return Response({"message": "완료"}, status=status.HTTP_200_OK)

           if user_plan_todo.finish_flag == 1: # 완료 -> 미완료인 경우
               user_plan_todo.finish_flag = 0;
               user_plan_todo.save()

               user_plan = User_Plan.objects.filter(user=user, plan_id=plan_id)[0]
               print(user_plan)

               user_plan_todos = User_plan_todo.objects.filter(user=user, plan_id=plan_id)
               res = 0
               i = 0
               for user_plan_todo in user_plan_todos:
                   res += user_plan_todo.finish_flag
                   i += 1
               user_plan.rate = (res / i) * 100
               user_plan.save()

               return Response({"message": "미완료"}, status=status.HTTP_200_OK)
           return Response({"error": "에러"}, status=status.HTTP_202_ACCEPTED)
       except:
           return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)