from django.core.serializers import get_serializer
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
# Create your views here.

class RegisterApi(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'status':status.HTTP_200_OK})
        return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
