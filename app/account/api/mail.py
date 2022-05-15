from rest_framework import generics,status
from django.contrib.auth.models import User
from account.serializers import (
                                SignUpMailSerializer,
                                ResetPasswordMailSerializer
                            )
from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.views import APIView
from rest_framework.response import Response


class SignUpMailAPIView(APIView):
    def post(self, request):
        serializer = SignUpMailSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordMailAPIView(APIView):
    """
    Send reset password Mail
    """
    def post(self, request):
        serializer = ResetPasswordMailSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
