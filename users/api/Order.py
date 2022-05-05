from business.models import Item,Order
from rest_framework import generics,status
from users.serializers import (
                                    UserOrderSerializer,
                                    OrderCreateSerializer,

                                    OrderInitializePaymentSerializer,
                                    OrderVerifyPaymentSerializer,
                                    OrderPaymentWithSavedCardSerializer,
                                )
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsEndUser
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
import json,hashlib,hmac

"""
    Order APIs
"""

class OrderAPIView(generics.ListAPIView):
    """
    Used only to list orders
    belonging to account
    """
    queryset = Order.objects.all()
    serializer_class = UserOrderSerializer
    permission_classes = [IsAuthenticated, IsEndUser]

    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(buyer=request.user.userProfile)
        serializer = UserOrderSerializer(queryset, many=True)
        return Response(serializer.data)
    

class OrderCreateAPIView(generics.CreateAPIView):
    """
    Create an order
    """
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated, IsEndUser]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderInitializePaymentAPIView(APIView):
    """
    Initialize payment for order
    """
    def post(self, request):
        serializer = OrderInitializePaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderVerifyPaymentAPIView(APIView):
    """
    Verify payment for order
    """
    def post(self, request):
        serializer = OrderVerifyPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderPaymentWithSavedCardAPIView(APIView):
    """
    Payment for order with saved card
    """
    def post(self, request):
        serializer = OrderPaymentWithSavedCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




"""
    Paystack Order Callback and Webhook
"""
    

class OrderPaystackWebhookAPIView(APIView):
    """
    Charge.Success webhook
    """
    def post(self, request):        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if ip_address in settings.PAYSTACK_WHITELISTED_IPS:
            hash_ = hmac.new(settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
                                msg=request.body,
                                digestmod=hashlib.sha512
                            ).hexdigest()
            data = request.data
            if hash_ == request.headers['X-Paystack-Signature']:
                if data.get('event')=='charge.success':
                    data = data.get('data')    
                    if data["status"]=="success":
                        order = Order.objects.get(reference=data.get('reference'))
                        order.payment_successful()
        return Response(status=status.HTTP_204_NO_CONTENT)