from urllib import request
from account.models.UserProfile import CardInformation
from business.models.Order import Item, Order, PurchasedItem
from core.module.paystack import Paystack
from rest_framework import serializers
from account.models import BusinessProfile
from account.module.generate_random import getRandomNumbers
from core.module.email import Email
from core.module.math import get_fees
from django.utils import timezone
from django.db import transaction
from django.conf import settings
import json


class PurchasedItemSerializer(serializers.ModelSerializer):
    """
    Only used internally
    """
    id = serializers.IntegerField()
    units = serializers.IntegerField()
    class Meta:
        fields = ("id","units",)
 




class OrderCreateSerializer(serializers.Serializer):
    seller = serializers.IntegerField()
    items = PurchasedItemSerializer(many=True)
   

    class Meta:
        fields = ("seller","items")
 
    def save(self):
        validated_data = self.validated_data
        seller = validated_data.get("seller")
        items = validated_data.get("items")
        total = 0
        purchased_items = []

        for item_data in items:
            if item_data.get("units") == 0:
                raise serializers.ValidationError({"items":"Item units must be greater than 0 "})
            
            item = Item.objects.get(id=item_data.get('id'))
            if item.owner != BusinessProfile.objects.get(pk=seller):
                raise serializers.ValidationError({"seller":"Seller does not own this item"})
            if item.units < item_data.get("units"):
                raise serializers.ValidationError({"items":"Requested for greater quantity than is available"})
            
            purchased_items.append({
                "item":item_data.get("id"),
                "units":item_data.get("units")
            })
            total += item.price * item_data.get("units")

        validated_data['buyer'] = self.context.get("request").user.businessProfile 
        validated_data['pin'] = getRandomNumbers(4) 
        validated_data['total'] = total 
        validated_data['status'] = 1 # AWAITING_PAYMENT
        validated_data["fees"] = get_fees(total)

        order = Order.objects.create(**validated_data)
        for purchased_item in purchased_items:
            purchased_item["order"] = order.id
        PurchasedItem.objects.bulk_create(**purchased_items)

        return order
    




class OrderInitializePaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField() # order id
    class Meta:
        fields = ("id")

    def save(self):
        order_id = self.validated_data.get("id")
        order = Order.objects.get(id=order_id)
        data = Paystack.initialize_payment(order)
        if not data:
            raise serializers.ValidationError({
                                "order":"Failed"
                            })
        # add reference
        order.reference = data.get('reference')
        order.save()

        return data




class OrderVerifyPaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    class Meta:
        fields = ("id")

    def save(self):
        order_id = self.validated_data.get("id")
        order = Order.objects.get(id=order_id)
        data = Paystack.verify_payment(order)
        
        if data!=False:
            transaction_status = data.get("status")
            if transaction_status == "success":
                return data

        raise serializers.ValidationError({
                                "order":"Failed"
                            })


class OrderPayStackSuccessCallbackSerializer(serializers.Serializer):
    
    def save(self):   
        reference = self.request.query_params.get('reference')
        order = Order.objects.get(reference=reference)
        order.payment_successful()

               

class OrderPaystackWebhookSerializer(serializers.Serializer):
    
    def save(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
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
                
        
        
         




class OrderPaymentWithSavedCardSerializer(serializers.Serializer):
    """
    Pay for order with a saved card
    """
    id = serializers.IntegerField()
    last4 = serializers.CharField()
    class Meta:
        fields = ("id","last4")

    
    def save(self):
        order_id = self.validated_data.get("id")
        last4 = self.validated_data.get("last4")
        order = Order.objects.get(id=order_id)
        card = CardInformation.objects.get(
                                        owner=order.buyer,
                                        last4= last4,
                                    )
        data = Paystack.pay_with_card(order,card)
        if not data:
            raise serializers.ValidationError({
                                "order":"Failed"
                            })

        reference = data.get('reference')
        order.payment_successful(reference=reference)    
        return data





class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    """
    Update order status from 'SENT' to 'READY' or 
                        from 'READY' to 'COLLECTED' 
    """
    status = serializers.IntegerField()
    pin = serializers.IntegerField(required=False,write_only=True)
   

    class Meta:
        model = Order
        fields = ("status","pin")

 
    def update(self,instance,validated_data):
        request = self.context.get("request")
        
        if instance.status==2: # 2 == SENT
            if validated_data.get("status") == 3: # 3 == READY
                user = request.user
                Email(request,user).send_business_order_ready_mail(instance)
                instance.status == 3
                instance.was_ready_by = timezone.now()
                instance.save()
            else:
                raise serializers.ValidationError({"status":"Incorrect order status"})
        

        elif instance.status == 3: # 3 == READY
            if validated_data.get("status") == 4:
                pin = validated_data.get("pin",None)
                if pin:
                    if pin == instance.pin:
                         with transaction.atomic():
                            business = (
                                            BusinessProfile.objects
                                            .select_for_update()
                                            .get(id=instance.seller.id)
                                        )
                            
                            business.total_earned +=  instance.total
                            business.save()
                         instance.status == 4 # 4 == COLLECTED
                         instance.save()
                    else:
                        raise serializers.ValidationError({"pin":"Incorrect pin"})
                else:
                    raise serializers.ValidationError({"pin":"Pin must be included"})
            else:
                raise serializers.ValidationError({"status":"Incorrect order status"})
        else:
            raise serializers.ValidationError("Order can't be updated here. CHeck the current order status before you try again")

        return instance
    