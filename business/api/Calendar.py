from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from business.models import Calendar
from business.serializers import (
                                        RetrieveUpdateCalendarSerializer
                                    )
from business.permissions import BusinessOnly
from django.shortcuts import get_object_or_404


class RetrieveUpdateCalendarAPIView(generics.RetrieveUpdateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = RetrieveUpdateCalendarSerializer
    permission_classes = [IsAuthenticated,BusinessOnly]

    def get_object(self):
        queryset = self.get_queryset() 
        filter_ = {"owner":self.request.user.businessProfile.pk}
        obj = get_object_or_404(queryset, **filter_)
        return obj
    

