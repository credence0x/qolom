from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from account.models import BusinessProfile
from account.serializers import (CreateBusinessProfileSerializer,
                            UpdateBusinessProfileSerializer,
                            BusinessProfileSerializer)
from django_filters.rest_framework import DjangoFilterBackend


class ListBusinessProfileAPIView(generics.ListAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country',"name","key","iso_code",
                        "minimum_age_allowed","state","address"]

    
class CreateBusinessProfileAPIView(generics.CreateAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = CreateBusinessProfileSerializer

class UpdateBusinessProfileAPIView(generics.UpdateAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = UpdateBusinessProfileSerializer
    permission_classes = [IsAuthenticated]
    
