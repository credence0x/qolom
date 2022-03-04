from business.models.Order import Item, Order, PurchasedItem
from rest_framework import serializers
from account.models import BusinessProfile
from account.module.generate_random import getRandomNumbers, getRandomKey


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
        validated_data['status'] = 1 # SENT

        order = Order.objects.create(**validated_data)
        for purchased_item in purchased_items:
            purchased_item["order"] = order.id
        PurchasedItem.objects.bulk_create(**purchased_items)

        return order
    
