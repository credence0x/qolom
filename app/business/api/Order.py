from business.models import Item,Order
from rest_framework import generics,status
from business.serializers import (
                                    ItemSerializer,
                                    CreateItemSerializer,
                                    UpdateDestroyItemSerializer,

                                    OrderSerializer,
                                    OrderUpdateStatusSerializer
                                    
                                )
from rest_framework.permissions import IsAuthenticated
from business.permissions import IsBusiness, IsObjectOwner,IsSeller
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


"""
    Item APIs
"""
class CreateItemAPIView(generics.CreateAPIView):

    queryset = Item.objects.all()
    serializer_class = CreateItemSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsObjectOwner]

    def post(self, request):
        serializer = CreateItemSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListItemAPIView(generics.ListAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsBusiness]

    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(owner=request.user.businessProfile)
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveItemAPIView(generics.RetrieveAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsBusiness]

    def get_object(self):
        queryset = self.get_queryset()
        filter_ = {"owner":self.request.user.businessProfile.pk}
        obj = get_object_or_404(queryset, **filter_)
        return obj



class UpdateItemAPIView(generics.UpdateAPIView):

    queryset = Item.objects.all()
    serializer_class = UpdateDestroyItemSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsObjectOwner]

class DestroyItemAPIView(generics.DestroyAPIView):

    queryset = Item.objects.all()
    serializer_class = UpdateDestroyItemSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsObjectOwner]




"""
    Order APIs
"""

class OrderListAPIView(generics.ListAPIView):
    """
    List all current orders or filter by status
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsBusiness]

    def list(self, request):
        status_list = [2,3,4]
        queryset = self.get_queryset()
        if "status" in request.query_params:
            status = request.query_params.get("status")
            status = int(status)
            queryset = queryset.filter(seller=request.user.businessProfile,
                                       status=status)
        else:
            queryset = queryset.filter(seller=request.user.businessProfile,
                                       status__in=status_list)

        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class OrderUpdateStatusAPIView(generics.UpdateAPIView):
    """
    update order status by status
    """
    queryset = Order.objects.all()
    serializer_class = OrderUpdateStatusSerializer
    permission_classes = [IsAuthenticated, IsBusiness, IsSeller]

   \

