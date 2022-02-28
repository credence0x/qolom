from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from account.models import UserProfile
from account.serializers import (CreateUserProfileSerializer,
                            UpdateUserProfileSerializer)

class CreateUserProfileAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = CreateUserProfileSerializer

class UpdateUserProfileAPIView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated]
    
