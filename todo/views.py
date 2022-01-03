from django.utils import timezone

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import accounts.views
from todo.models import Personal_todo
from todo.serializers import PersonalTodoSerializer


# pk로 유저 정보 확인, 해당 유저의 todos 항목 존재 여부 확인 메소드
def check_invalid_todo(pk):
    accounts.views.get_user(pk)
    personal_todos = Personal_todo.objects.filter(user_id=pk)
    return personal_todos


class PersonalTodoView(APIView):
    def get(self, request, pk):
        try:
            serializer = PersonalTodoSerializer(check_invalid_todo(pk), many=True)
            return JsonResponse(
                [{"미완료": PersonalTodoSerializer(check_invalid_todo(pk).filter(finish_flag=False), many=True).data},
                {"완료": PersonalTodoSerializer(check_invalid_todo(pk).filter(finish_flag=True), many=True).data},
                {"전체": serializer.data}],
                status=status.HTTP_201_CREATED, safe=False)

        except ValueError:
            return JsonResponse({'error message': '데이터가 없습니다.'})
