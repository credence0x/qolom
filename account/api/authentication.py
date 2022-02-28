from rest_framework import status
from account.serializers import (
                            CheckResetPasswordLinkSerializer,
                            )
from rest_framework.views import APIView
from rest_framework.response import Response


class CheckResetPasswordLinkAPIView(APIView):
    """
    Check that reset password link is valid
    """
    def get(self, request):
        params = request.query_params
        uidb64,token = params.get("uidb64",None),params.get("token",None)
        
        request.data["uidb64"]= uidb64
        request.data["token"]=token
        
        serializer = CheckResetPasswordLinkSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
