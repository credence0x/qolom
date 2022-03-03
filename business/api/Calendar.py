from urllib import request
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from business.models import Calendar
from business.serializers import (
                                        CreateCalendarSerializer,
                                        RetrieveUpdateDestroyCalendarSerializer
                                    )
from business.permissions import BusinessOnly
from django.shortcuts import get_object_or_404

class CreateCalendarAPIView(generics.CreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CreateCalendarSerializer
    permission_classes = [IsAuthenticated,BusinessOnly]


class RetrieveUpdateDestroyCalendarAPIView(generics.UpdateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = RetrieveUpdateDestroyCalendarSerializer
    permission_classes = [IsAuthenticated,BusinessOnly]

    def get_object(self):
        queryset = self.get_queryset() 
        obj = get_object_or_404(queryset, {"owner":request.user.businessProfile.pk})
        return obj
    

