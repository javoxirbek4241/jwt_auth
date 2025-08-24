from importlib.resources import read_text

from django.contrib.auth import authenticate
from django.core.serializers import get_serializer
from django.shortcuts import render
from django.template.base import VARIABLE_TAG_START
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import permissions
# Create your views here.

class RegisterApi(GenericAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        data = request.data
        password = data['password']
        password2 = data['password2']
        if password!=password2:
            raise ValidationError('parollar mos emas')
        username = data['username']
        email = data['email']
        CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return Response({
            'msg':"Ro'yxatdan o'tildi",
            'status':status.HTTP_201_CREATED
        })


        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({'data': serializer.data, 'status':status.HTTP_200_OK})
        # return Response({'error':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})


class LoginApi(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        if not CustomUser.objects.filter(email=email).exists():
            return Response({
                'error':"bunday foydalanuvchi mavjud emas",
                'status':status.HTTP_400_BAD_REQUEST
            })
        user = authenticate(email=email, password = password)
        token = RefreshToken.for_user(user)
        data = {
            'refresh':str(token),
            'access' : str(token.access_token)
        }

        return Response(data=data)

class LogoutApi(APIView):
    def post(self, request):
        data = request.data
        try:
            token=RefreshToken(data['refresh'])
            token.blacklist()
            return Response({'msg':"Chiqdingiz"})
        except Exception as e:
            return Response({
                'error':str(e)
            })



class RefreshTok(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        try:
            token=RefreshToken(data['refresh'])
            return Response({'msg':"Chiqdingiz", 'access':str(token.access_token)})
        except Exception as e:
            return Response({
                'error':str(e)
            })