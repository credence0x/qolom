from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ...models import UserProfile
from ...serializers import (CreateUserProfileSerializer,
                            UpdateUserProfileSerializer)

class CreateUserProfileAPIView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = CreateUserProfileSerializer

class UpdateUserProfileAPIView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated]
    
