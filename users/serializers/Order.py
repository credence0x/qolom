from urllib import request
from account.models.UserProfile import CardInformation
from business.models.Order import Item, Order, PurchasedItem
from core.module.paystack import Paystack
from rest_framework import serializers
from account.models import BusinessProfile
from account.module.generate_random import getRandomNumbers
from core.module.math import get_fees

from django.conf import settings
import json





 




class OrderCreateSerializer(serializers.Serializer):
    class PurchasedItemSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField()
        units = serializers.IntegerField()
        class Meta:
            fields = ("id","units",)


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