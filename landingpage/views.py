from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import landingPage
from rest_framework.permissions import AllowAny


# 랜딩 페이지 폼 등록
class landingpageView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            phoneNum = request.data['phoneNum']
            job = request.data['job']
            todoPlan = request.data['todoPlan']
            form = landingPage(phoneNum=phoneNum, job=job, todoPlan=todoPlan)
            form.save()
            return Response({"message": "등록 완료"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "에러가 발생했습니다."}, status=status.HTTP_400_BAD_REQUEST)