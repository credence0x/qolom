from business.models import Item,Order
from rest_framework import generics,status
from users.serializers import (
                                    
                                    OrderCreateSerializer,

                                    OrderInitializePaymentSerializer,
                                    OrderVerifyPaymentSerializer,
                                    OrderPaymentWithSavedCardSerializer,
                                    OrderPayStackSuccessCallbackSerializer,
                                    OrderPaystackWebhookSerializer,
                                )
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsEndUser
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
import json

"""
    Order APIs
"""

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
class OrderPayStackSuccessCallbackAPIView(APIView):
    """
    Charge.Success callback
    """
    def get(self, request):
        reference = request.query_params.get('reference')
        order = Order.objects.get(reference=reference)
        order.payment_successful()
        return Response({}, status=status.HTTP_200_OK)
        
        

class OrderPaystackWebhookAPIView(APIView):
    """
    Charge.Success webhook
    """
    def get(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if ip_address in settings.PAYSTACK_WHITELISTED_IPS: 
            req_body = request.body.decode('utf-8')
            body = json.loads(req_body)
            if body.get('event')=='charge.success':
                data = body.get('data')                  
                order = Order.objects.get(reference=data.get('reference'))
                order.payment_successful()
            return Response({}, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)