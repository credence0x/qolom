from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from ...models import UserProfile
from django.contrib.auth.models import User
from ...serializers import (
                            AuthenticateUserProfileSerializer,
                            DeauthenticateUserProfileSerializer,
                            ActivateUserProfileTokenSerializer,

                            )
from rest_framework.views import APIView
from rest_framework.response import Response



class ActivateUserProfileTokenAPIView(APIView):
    """
    Activate UserProfile account by confirming tokens sent via email
    """
    def get(self, request):
        params = request.query_params
        uidb64,token = params.get("uidb64",None),params.get("token",None)
        params_data = {"uidb64":uidb64,
                        "token":token}
        serializer = ActivateUserProfileTokenSerializer(data=params_data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateUserProfileAPIView(APIView):
    """
    Log in a UserProfile model
    """
    def post(self, request):
        serializer = AuthenticateUserProfileSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeauthenticateUserProfileAPIView(APIView):
    """
    Log out a UserProfile model
    """
    def post(self, request):
        serializer = DeauthenticateUserProfileSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

