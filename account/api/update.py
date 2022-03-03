from rest_framework import generics,status
from django.contrib.auth.models import User
from account.serializers import (
                            ResetPasswordSerializer,
                            CheckResetPasswordLinkSerializer,
                            ChangePasswordSerializer,
                            )
from rest_framework.views import APIView
from rest_framework.response import Response

class ResetPasswordAPIView(APIView):
    """
    Update password using mail link
    """
    def post(self, request):
        params = request.query_params
        uidb64,token = params.get("uidb64",None),params.get("token",None)
        request.data["uidb64"]= uidb64
        request.data["token"]=token

        serializer = ResetPasswordSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordAPIView(APIView):
    """
    Update password of logged in user
    """
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

