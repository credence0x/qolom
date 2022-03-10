from account.models.UserProfile import CardInformation
from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CardInformation
        exclude = ("owner",)

    def create(self,validated_data):
        owner = self.context.get("request").user.userProfile
        validated_data["owner"] = owner
        return CardInformation.objects.create(**validated_data)


    