from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from business.models import BusinessQueue
from business.serializers import (
                                        CreateQueueSerializer,
                                        RetrieveQueueSerializer,
                                        UpdateDestroyQueueSerializer,
                                        RetrieveQueueInformationSerializer
                                    )
from business.permissions import  IsBusiness, IsBusinessOwner

class CreateQueueAPIView(generics.CreateAPIView):
    queryset = BusinessQueue.objects.all()
    serializer_class = CreateQueueSerializer
    permission_classes = [IsAuthenticated, IsBusiness]


class RetrieveQueueAPIView(generics.RetrieveAPIView):
    """
    Retrieve the list of people in a single queue
    """
    queryset = BusinessQueue.objects.all()
    serializer_class = RetrieveQueueSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsBusinessOwner]

class RetrieveQueueInformationAPIView(generics.RetrieveAPIView):
    """
    For retrieving the basic queue information
     e.g name,instruction, information and key
    """
    queryset = BusinessQueue.objects.all()
    serializer_class = RetrieveQueueInformationSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsBusinessOwner]

    

class UpdateQueueAPIView(generics.UpdateAPIView):
    queryset = BusinessQueue.objects.all()
    serializer_class = UpdateDestroyQueueSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsBusinessOwner]

class DestroyQueueAPIView(generics.DestroyAPIView):
    queryset = BusinessQueue.objects.all()
    serializer_class = UpdateDestroyQueueSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsBusinessOwner]