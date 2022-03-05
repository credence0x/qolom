from urllib import request
from business.models.Order import Item, Order, PurchasedItem
from rest_framework import serializers
from account.models import BusinessProfile
from account.module.generate_random import getRandomNumbers, getRandomKey
from core.module.email import Email
from django.utils import timezone
from django.db import transaction

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ("name","price","units",)
 

    


class CreateItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("name","price","units",)
 
    def create(self,validated_data):
        validated_data['owner'] = self.context.get("request").user.businessProfile 
        item = Item.objects.create(**validated_data)
        return item
    

class UpdateDestroyItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("name","price","units",)


class PurchasedItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    units = serializers.IntegerField()
    class Meta:
        fields = ("id","units",)
 




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("buyer","seller","items","status")
        depth = 2 

    
    
class CreateOrderSerializer(serializers.Serializer):
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
        validated_data['reference'] = getRandomKey(25) 
        validated_data['pin'] = getRandomNumbers(4) 
        validated_data['total'] = total 
        validated_data['status'] = 1 # AWAITING_PAYMENT

        order = Order.objects.create(**validated_data)
        for purchased_item in purchased_items:
            purchased_item["order"] = order.id
        PurchasedItem.objects.bulk_create(**purchased_items)

        return order
    



class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField()
    pin = serializers.IntegerField(required=False,write_only=True)
   

    class Meta:
        fields = ("status","pin")

 
    def update(self,instance,validated_data):
        request = self.context.get("request")
        
        if instance.status==2: # 2 == SENT
            if validated_data.get("status") == 3: # 3 == READY
                user = request.user
                Email(request,user).send_order_ready_mail(instance)
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
    