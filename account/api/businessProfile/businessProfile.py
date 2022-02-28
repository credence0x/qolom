from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from account.models import BusinessProfile
from account.serializers import (CreateBusinessProfileSerializer,
                            UpdateBusinessProfileSerializer)

class CreateBusinessProfileAPIView(generics.CreateAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = CreateBusinessProfileSerializer

class UpdateBusinessProfileAPIView(generics.UpdateAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = UpdateBusinessProfileSerializer
    permission_classes = [IsAuthenticated]
    
