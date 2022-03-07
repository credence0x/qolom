from account.models import CardInformation
from rest_framework import generics
from users.permissions import IsObjectOwner
from users.serializers import (     
                                    CardSerializer
                                )
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsEndUser, IsObjectOwner

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


class RetrieveUpdateDestroyCardAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete card
    """
    queryset = CardInformation.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated, IsEndUser, IsObjectOwner]