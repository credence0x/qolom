from asyncore import write
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
        units = serializers.IntegerField(min_value=1)
        class Meta:
            model = Item
            fields = ("id","units",)


    seller = serializers.IntegerField()
    items = PurchasedItemSerializer(many=True)
    id = serializers.IntegerField(read_only=True)
   

    class Meta:
        fields = ("seller","items")
 
    def save(self):
        validated_data = self.validated_data.copy()
        seller = BusinessProfile.objects.get(id=validated_data.get("seller"))
        items = validated_data.get("items")
        total = 0
        purchased_items = []
        
        for raw_item_data in items:
            if raw_item_data.get("units") == 0:
                raise serializers.ValidationError({"items":"Item units must be greater than 0 "})
            
            item = Item.objects.get(id=raw_item_data.get('id'))
            if item.owner != seller:
                raise serializers.ValidationError({"seller":"Seller does not own this item"})
            if item.units < raw_item_data.get("units"):
                raise serializers.ValidationError({"items":"Requested for greater quantity than is available"})
            
            purchased_items.append(
                PurchasedItem(
                    item=item,
                    units=raw_item_data.get("units"),
                    is_active = True
                )
               )
            total += item.price * raw_item_data.get("units")


        validated_data['buyer'] = self.context.get("request").user.userProfile
        validated_data['pin'] = getRandomNumbers(4) 
        validated_data['total'] = total 
        validated_data['status'] = 1 # AWAITING_PAYMENT
        validated_data["fees"] = get_fees(total)
        validated_data["seller"] = seller

        del validated_data["items"]

        order = Order.objects.create(**validated_data)
        for purchased_item in purchased_items:
            setattr(purchased_item,"order",order)
        PurchasedItem.objects.bulk_create(purchased_items)
        
        self.validated_data["id"] = order.id
        return 
    




class OrderInitializePaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField() # order id
    data = serializers.DictField(child=serializers.CharField(),read_only=True)
    class Meta:
        fields = ("id","data")

    def save(self):
        order_id = self.validated_data.get("id")
        order = Order.objects.get(id=order_id)
        data = Paystack().initialize_payment(order)
        if not data:
            raise serializers.ValidationError({
                                "order":"Failed"
                            })
        # add reference
        order.reference = data.get('reference')
        order.save()

        self.validated_data["data"] = data

        return 




class OrderVerifyPaymentSerializer(serializers.Serializer):
    reference = serializers.CharField()
    success = serializers.BooleanField(read_only=True)
    class Meta:
        fields = ("reference","success")

    def save(self):
        reference = self.validated_data.get("reference")
        order = Order.objects.get(reference=reference)
        data = Paystack().verify_payment(order)
        self.validated_data["success"] = False
        if data!=False:
            transaction_status = data.get("status")
            if transaction_status == "success":
                self.validated_data["success"] = True
        


                
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
        data = Paystack().pay_with_card(order,card)
        if not data:
            raise serializers.ValidationError({
                                "order":"Failed"
                            })

        reference = data.get('reference')
        order.payment_successful(reference=reference)    
        return data