from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions,authentication
from .serializers import RegisterSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class Login(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request):
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            user.save()
            token,c = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},200)
        except Exception as e:
            return Response({"error":str(e)},400)


class Register(APIView):
    permission_classes=[permissions.AllowAny]

    def post(self,request):
        try:
            serializer = RegisterSerializer(data=request.data)
            
            serializer.is_valid(raise_exception=True)
            user1 = serializer.save()
            token=Token.objects.create(user=user1)
            return Response({
                "user": UserSerializer(user1).data,
                "token": token.key
            },200)
        except Exception as e:
            return Response({"error":str(e)},400)


class Logout(APIView):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]

    def post(self,request):
        try:
            token=Token.objects.get(user=request.user)
            token.delete()
            return Response({"message":"Logout successfull"},200)
        except Exception as e:
            return Response({"error":str(e)},400)

