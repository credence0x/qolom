from ast import Or
from dataclasses import field
from urllib import request
from account.models.UserProfile import CardInformation
from business.models.Order import Item, Order, PurchasedItem
from core.module.paystack import Paystack
from rest_framework import serializers
from account.models import BusinessProfile
from account.module.generate_random import getRandomNumbers, getRandomKey
from core.module.email import Email
from core.module.math import get_fees
from django.utils import timezone
from django.db import transaction
from django.conf import settings
import json


"""
    Item Serializers
"""
class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ("name","price","units",)
 

class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("name","price","units",)

    def validate_name(self,value):
        business = self.context.get("request").user.businessProfile
        item = Item.objects.filter(owner=business,name=value)
        if item.exists():
            raise serializers.ValidationError(
                    "An item with a matching name already exists"
                )
        return value 



    def create(self,validated_data):
        validated_data['owner'] = self.context.get("request").user.businessProfile 
        item = Item.objects.create(**validated_data)
        return item
    

class UpdateDestroyItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("name","price","units",)




"""
    Order Serializers
"""

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("buyer","seller","items","status")
        depth = 2 

    
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
    