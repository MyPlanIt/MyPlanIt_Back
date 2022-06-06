from django.shortcuts import render
from .models import Notice
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import NoticeSerializer

# Create your views here.


class NoticeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            notice = Notice.objects.order_by('-created_at')  # 최신순 정렬
            notice_serializer = NoticeSerializer(notice, many=True).data
            return Response({"Notice": notice_serializer}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "error"}, status=status.HTTP_202_ACCEPTED)