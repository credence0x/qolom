from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from business.models import BusinessQueue
from business.serializers import (
                                        CreateQueueSerializer,
                                        RetrieveQueueSerializer,
                                        UpdateDestroyQueueSerializer,
                                        RetrieveQueueInformationSerializer
                                    )
from business.permissions import BusinessOnly

class CreateQueueAPIView(generics.CreateAPIView):
    queryset = BusinessQueue.objects.all()
    serializer_class = CreateQueueSerializer
    permission_classes = [IsAuthenticated,BusinessOnly]


class RetrieveQueueAPIView(generics.UpdateAPIView):
    """
    Retrieve the list of people in a single queue
    """
    queryset = BusinessQueue.objects.all()
    serializer_class = RetrieveQueueSerializer
    permission_classes = [IsAuthenticated,BusinessOnly]

class RetrieveQueueInformationAPIView(generics.UpdateAPIView):
    """
    For retrieving the basic queue information
     e.g name,instruction, information and key
    """
    queryset = BusinessQueue.objects.all()
    serializer_class = RetrieveQueueInformationSerializer
    permission_classes = [IsAuthenticated,BusinessOnly]

    

class UpdateDestroyQueueAPIView(generics.UpdateAPIView):
    queryset = BusinessQueue.objects.all()
    serializer_class = UpdateDestroyQueueSerializer
    permission_classes = [IsAuthenticated,BusinessOnly]

