from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from account.models import BusinessProfile
from django.contrib.auth.models import User
from account.serializers import (
                            AuthenticateBusinessProfileSerializer,
                            DeauthenticateBusinessProfileSerializer,
                            ActivateBusinessProfileTokenSerializer,

                            )
from rest_framework.views import APIView
from rest_framework.response import Response



class ActivateBusinessProfileTokenAPIView(APIView):
    """
    Activate BusinessProfile account by confirming tokens sent via email
    """
    def get(self, request):
        params = request.query_params
        uidb64,token = params.get("uidb64",None),params.get("token",None)
        params_data = {"uidb64":uidb64,
                        "token":token}
        serializer = ActivateBusinessProfileTokenSerializer(data=params_data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateBusinessProfileAPIView(APIView):
    """
    Log in a BusinessProfile model
    """
    def post(self, request):
        serializer = AuthenticateBusinessProfileSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeauthenticateBusinessProfileAPIView(APIView):
    """
    Log out a BusinessProfile model
    """
    def post(self, request):
        serializer = DeauthenticateBusinessProfileSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

