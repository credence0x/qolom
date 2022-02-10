from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from ...models import UserProfile
from django.contrib.auth.models import User
from ...serializers import (
                            AuthenticateUserSerializer,
                            DeauthenticateUserSerializer
                            )
from rest_framework.views import APIView
from rest_framework.response import Response

class AuthenticateUserProfileAPIView(APIView):
    queryset = User.objects.all()

    def post(self, request):
        serializer = AuthenticateUserSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeauthenticateUserProfileAPIView(APIView):
    queryset = User.objects.all()

    def post(self, request):
        serializer = DeauthenticateUserSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


