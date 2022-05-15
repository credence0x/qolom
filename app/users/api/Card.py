from account.models import CardInformation
from rest_framework import generics,status
from users.permissions import IsObjectOwner
from users.serializers import (     
                                    CardSerializer
                                )
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsEndUser, IsObjectOwner
from rest_framework.response import Response


"""
    Card Information APIs
"""

class CreateCardAPIView(generics.ListCreateAPIView):
    """
    Create or list card
    """
    queryset = CardInformation.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsEndUser]

    def post(self, request):
        serializer = CardSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUpdateDestroyCardAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete card
    """
    queryset = CardInformation.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsEndUser, IsObjectOwner]